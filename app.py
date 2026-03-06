from flask import Flask, render_template, request, redirect, session, abort
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "fitcenter_secret"


# -------------------------
# CONEXÃO BANCO
# -------------------------

def conectar():
    return sqlite3.connect("fitcenter.db")


# -------------------------
# CRIAR BANCO
# -------------------------

def criar_banco():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT UNIQUE,
        senha TEXT,
        tipo TEXT,
        aluno_id INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        peso REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treinos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        nome TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercicios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        treino_id INTEGER,
        exercicio TEXT,
        series INTEGER,
        repeticoes INTEGER,
        carga TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avaliacoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        peso REAL,
        gordura REAL,
        massa REAL,
        data TEXT
    )
    """)

    conn.commit()

    senha_hash = generate_password_hash("341062")

    cursor.execute("""
    INSERT OR IGNORE INTO usuarios
    (id,nome,email,senha,tipo)
    VALUES
    (1,'Suporte','suportesuper@gmail.com',?,'suporte')
    """,(senha_hash,))

    conn.commit()
    conn.close()


criar_banco()


# -------------------------
# LOGIN
# -------------------------

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM usuarios WHERE email=?",
            (email,)
        )

        usuario = cursor.fetchone()

        conn.close()

        if usuario and check_password_hash(usuario[3], senha):

            session["usuario_id"] = usuario[0]
            session["nome"] = usuario[1]
            session["tipo"] = usuario[4]
            session["aluno_id"] = usuario[5]

            return redirect("/")

        return "Login inválido"

    return render_template("login.html")


# -------------------------
# LOGOUT
# -------------------------

@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")


# -------------------------
# DASHBOARD
# -------------------------

@app.route("/")
def dashboard():

    if "usuario_id" not in session:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM alunos")
    total_alunos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM treinos")
    total_treinos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM avaliacoes")
    total_avaliacoes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total_usuarios = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total_alunos=total_alunos,
        total_treinos=total_treinos,
        total_avaliacoes=total_avaliacoes,
        total_usuarios=total_usuarios
    )


# -------------------------
# LISTA DE ALUNOS
# -------------------------

@app.route("/alunos")
def alunos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()

    conn.close()

    return render_template("lista_alunos.html", alunos=alunos)


# -------------------------
# CADASTRAR ALUNO
# -------------------------

@app.route("/cadastro", methods=["GET","POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO alunos (nome,email) VALUES (?,?)",
            (nome,email)
        )

        conn.commit()
        conn.close()

        return redirect("/alunos")

    return render_template("cadastro_aluno.html")


# -------------------------
# TREINOS DO ALUNO
# -------------------------

@app.route("/treino/<int:aluno_id>", methods=["GET","POST"])
def treino(aluno_id):

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":

        nome = request.form["nome"]

        cursor.execute("""
        INSERT INTO treinos (aluno_id,nome)
        VALUES (?,?)
        """,(aluno_id,nome))

        conn.commit()

    cursor.execute("""
    SELECT id,nome
    FROM treinos
    WHERE aluno_id=?
    """,(aluno_id,))

    treinos = cursor.fetchall()

    conn.close()

    return render_template(
        "treino.html",
        treinos=treinos,
        aluno_id=aluno_id
    )


# -------------------------
# EXERCÍCIOS DO TREINO
# -------------------------

@app.route("/exercicios/<int:treino_id>", methods=["GET","POST"])
def exercicios(treino_id):

    conn = conectar()
    cursor = conn.cursor()

    if request.method == "POST":

        exercicio = request.form["exercicio"]
        series = request.form["series"]
        repeticoes = request.form["repeticoes"]
        carga = request.form["carga"]

        cursor.execute("""
        INSERT INTO exercicios
        (treino_id,exercicio,series,repeticoes,carga)
        VALUES (?,?,?,?,?)
        """,(treino_id,exercicio,series,repeticoes,carga))

        conn.commit()

    cursor.execute("""
    SELECT exercicio,series,repeticoes,carga
    FROM exercicios
    WHERE treino_id=?
    """,(treino_id,))

    exercicios = cursor.fetchall()

    conn.close()

    return render_template(
        "exercicios.html",
        exercicios=exercicios,
        treino_id=treino_id
    )


# -------------------------
# PERFIL DO ALUNO
# -------------------------

@app.route("/perfil/<int:id>")
def perfil(id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alunos WHERE id=?", (id,))
    aluno = cursor.fetchone()

    cursor.execute("""
        SELECT peso,gordura,massa,data
        FROM avaliacoes
        WHERE aluno_id=?
        ORDER BY data
    """,(id,))

    avaliacoes = cursor.fetchall()

    conn.close()

    datas = [a[3] for a in avaliacoes]
    pesos = [a[0] for a in avaliacoes]
    gorduras = [a[1] for a in avaliacoes]
    massas = [a[2] for a in avaliacoes]

    return render_template(
        "perfil.html",
        aluno=aluno,
        datas=datas,
        pesos=pesos,
        gorduras=gorduras,
        massas=massas
    )


# -------------------------
# ATUALIZAR PESO
# -------------------------

@app.route("/peso", methods=["POST"])
def atualizar_peso():

    if "aluno_id" not in session:
        return redirect("/login")

    peso = request.form["peso"]
    aluno_id = session["aluno_id"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE alunos SET peso=? WHERE id=?",
        (peso,aluno_id)
    )

    conn.commit()
    conn.close()

    return redirect(f"/perfil/{aluno_id}")


# -------------------------
# RODAR SERVIDOR
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)