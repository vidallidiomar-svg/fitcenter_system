from flask import Flask, render_template, request, redirect, session
from database import conectar, criar_banco
from niveis import calcular_nivel

app = Flask(__name__)
app.secret_key = "fitcenter_secret"

criar_banco()


# -------------------------------
# DASHBOARD
# -------------------------------

@app.route("/")
def dashboard():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM alunos")
    total_alunos = cursor.fetchone()["total"]

    cursor.execute("SELECT SUM(xp) as total FROM alunos")
    xp_total = cursor.fetchone()["total"] or 0

    cursor.execute("SELECT COUNT(*) as total FROM historico_treino")
    total_treinos = cursor.fetchone()["total"]

    conn.close()

    return render_template(
        "dashboard.html",
        total_alunos=total_alunos,
        xp_total=xp_total,
        total_treinos=total_treinos
    )


# -------------------------------
# CADASTRO ALUNO
# -------------------------------

@app.route("/cadastro", methods=["GET","POST"])
def cadastro():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        genero = request.form["genero"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO alunos (nome,email,genero)
        VALUES (?,?,?)
        """,(nome,email,genero))

        conn.commit()
        conn.close()

        return redirect("/alunos")

    return render_template("cadastro_aluno.html")


# -------------------------------
# LISTA ALUNOS
# -------------------------------

@app.route("/alunos")
def alunos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()

    conn.close()

    return render_template(
        "lista_alunos.html",
        alunos=alunos
    )


# -------------------------------
# PERFIL ALUNO
# -------------------------------

@app.route("/perfil/<int:aluno_id>")
def perfil(aluno_id):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nome,email,genero,xp,streak
    FROM alunos
    WHERE id=?
    """,(aluno_id,))

    aluno = cursor.fetchone()

    nivel = calcular_nivel(aluno["xp"], aluno["genero"])

    conquistas = []

    if aluno["xp"] >= 50:
        conquistas.append("Primeiro treino")

    if aluno["xp"] >= 200:
        conquistas.append("Discípulo do Ferro")

    if aluno["xp"] >= 500:
        conquistas.append("Guerreiro da Academia")

    if aluno["streak"] >= 5:
        conquistas.append("🔥 5 dias de treino")

    cursor.execute("""
    SELECT peso,gordura,massa,data
    FROM avaliacoes
    WHERE aluno_id=?
    ORDER BY data
    """,(aluno_id,))

    dados = cursor.fetchall()

    pesos=[]
    gorduras=[]
    massas=[]
    datas=[]

    for d in dados:

        pesos.append(d["peso"])
        gorduras.append(d["gordura"])
        massas.append(d["massa"])
        datas.append(d["data"])

    cursor.execute("""
    SELECT exercicio,peso,data
    FROM historico_treino
    WHERE aluno_id=?
    ORDER BY data DESC
    """,(aluno_id,))

    historico = cursor.fetchall()

    conn.close()

    return render_template(
        "perfil.html",
        aluno=aluno,
        nivel=nivel,
        conquistas=conquistas,
        pesos=pesos,
        gorduras=gorduras,
        massas=massas,
        datas=datas,
        historico=historico
    )


# -------------------------------
# REGISTRAR TREINO
# -------------------------------

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


# -------------------------------
# RANKING GERAL
# -------------------------------

@app.route("/ranking")
def ranking():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nome,xp,genero
    FROM alunos
    ORDER BY xp DESC
    """)

    ranking = cursor.fetchall()

    conn.close()

    return render_template(
        "ranking.html",
        ranking=ranking
    )


# -------------------------------
# RANKING SEMANAL
# -------------------------------

@app.route("/ranking_semanal")
def ranking_semanal():

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

    return render_template(
        "ranking_semanal.html",
        ranking=ranking
    )


# -------------------------------
# INICIAR APP
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)