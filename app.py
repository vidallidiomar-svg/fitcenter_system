from flask import Flask, render_template, request, redirect, session
import sqlite3
from database import criar_banco

app = Flask(__name__)
app.secret_key = "fitcenter_secret"

criar_banco()


def conectar():
    conn = sqlite3.connect("fitcenter.db")
    conn.row_factory = sqlite3.Row
    return conn


def calcular_nivel(xp):

    if xp >= 1200:
        return "Divindade do Aço"
    elif xp >= 800:
        return "Titã"
    elif xp >= 500:
        return "Forjador(a)"
    elif xp >= 250:
        return "Guerreiro(a)"
    elif xp >= 100:
        return "Aprendiz"
    else:
        return "Iniciante"


@app.route("/")
def dashboard():

    if "usuario_id" not in session:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM alunos")
    total_alunos = cursor.fetchone()["total"]

    cursor.execute("SELECT SUM(xp) as total FROM alunos")
    xp_total = cursor.fetchone()["total"] or 0

    cursor.execute("SELECT COUNT(*) as total FROM historico_treino")
    total_treinos = cursor.fetchone()["total"]

    cursor.execute("""
    SELECT data, COUNT(*) as total
    FROM historico_treino
    GROUP BY data
    ORDER BY data
    """)

    dados = cursor.fetchall()

    datas = []
    treinos = []

    for d in dados:
        datas.append(d["data"])
        treinos.append(d["total"])

    conn.close()

    return render_template(
        "dashboard.html",
        total_alunos=total_alunos,
        xp_total=xp_total,
        total_treinos=total_treinos,
        datas=datas,
        treinos=treinos
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM usuarios
        WHERE email=? AND senha=?
        """,(email,senha))

        usuario = cursor.fetchone()

        conn.close()

        if usuario:

            session["usuario_id"] = usuario["id"]
            session["tipo"] = usuario["tipo"]

            return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


@app.route("/cadastro", methods=["GET","POST"])
def cadastro():

    if "usuario_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO alunos
        (nome,email,xp,streak)
        VALUES (?,?,0,0)
        """,(nome,email))

        conn.commit()
        conn.close()

        return redirect("/alunos")

    return render_template("cadastro_aluno.html")


@app.route("/alunos")
def alunos():

    if "usuario_id" not in session:
        return redirect("/login")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alunos")

    alunos = cursor.fetchall()

    conn.close()

    return render_template("lista_alunos.html", alunos=alunos)


@app.route("/perfil/<int:aluno_id>")
def perfil(aluno_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alunos WHERE id=?", (aluno_id,))
    aluno = cursor.fetchone()

    nivel = calcular_nivel(aluno["xp"])

    cursor.execute("""
    SELECT peso,gordura,massa,data
    FROM avaliacoes
    WHERE aluno_id=?
    ORDER BY data
    """,(aluno_id,))

    avaliacoes = cursor.fetchall()

    pesos = []
    gorduras = []
    massas = []
    datas = []

    for a in avaliacoes:
        pesos.append(a["peso"])
        gorduras.append(a["gordura"])
        massas.append(a["massa"])
        datas.append(a["data"])

    conn.close()

    return render_template(
        "perfil.html",
        aluno=aluno,
        nivel=nivel,
        pesos=pesos,
        gorduras=gorduras,
        massas=massas,
        datas=datas
    )


@app.route("/avaliacao/<int:aluno_id>", methods=["GET","POST"])
def avaliacao(aluno_id):

    if request.method == "POST":

        peso = request.form["peso"]
        gordura = request.form["gordura"]
        massa = request.form["massa"]
        data = request.form["data"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO avaliacoes
        (aluno_id,peso,gordura,massa,data)
        VALUES (?,?,?,?,?)
        """,(aluno_id,peso,gordura,massa,data))

        conn.commit()
        conn.close()

        return redirect(f"/perfil/{aluno_id}")

    return render_template("avaliacao.html")


@app.route("/registrar_treino/<int:aluno_id>", methods=["POST"])
def registrar_treino(aluno_id):

    exercicio = request.form["exercicio"]
    peso = request.form["peso"]

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO historico_treino
    (aluno_id,exercicio,peso,data)
    VALUES (?,?,?,DATE('now'))
    """,(aluno_id,exercicio,peso))

    cursor.execute("""
    UPDATE alunos
    SET xp = xp + 20,
        streak = streak + 1
    WHERE id=?
    """,(aluno_id,))

    conn.commit()
    conn.close()

    return redirect(f"/perfil/{aluno_id}")


@app.route("/ranking")
def ranking():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nome,xp
    FROM alunos
    ORDER BY xp DESC
    LIMIT 10
    """)

    ranking = cursor.fetchall()

    conn.close()

    return render_template("ranking.html", ranking=ranking)


if __name__ == "__main__":
    app.run(debug=True)