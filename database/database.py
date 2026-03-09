import sqlite3


def conectar():

    conn = sqlite3.connect("fitcenter.db")
    conn.row_factory = sqlite3.Row

    criar_tabelas(conn)
    criar_usuario_suporte_padrao(conn)

    return conn


def criar_tabelas(conn):

    cursor = conn.cursor()

    # =========================
    # USUÁRIOS DO SISTEMA
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT UNIQUE,
        senha TEXT,
        perfil TEXT

    )
    """)

    # =========================
    # ALUNOS
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        apelido TEXT,
        email TEXT,
        senha TEXT,
        genero TEXT,
        foto TEXT,
        xp INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0

    )
    """)

    # =========================
    # TREINOS
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treinos(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        nome TEXT,
        arquivo_pdf TEXT,
        data_envio TEXT,
        concluido INTEGER DEFAULT 0

    )
    """)

    # =========================
    # EXERCÍCIOS DO TREINO
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treino_exercicios(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        treino_id INTEGER,

        ordem INTEGER,
        nome TEXT,

        series TEXT,
        repeticoes TEXT,
        intervalo TEXT,
        peso TEXT,
        movimento TEXT,
        metodo TEXT,

        peso_aluno TEXT,
        observacao_aluno TEXT,

        concluido INTEGER DEFAULT 0

    )
    """)

    # =========================
    # PLANOS ALIMENTARES
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS planos_alimentares(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        arquivo TEXT,
        data_envio TEXT

    )
    """)

    # =========================
    # AVALIAÇÕES
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avaliacoes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        arquivo TEXT,
        data_envio TEXT

    )
    """)

    conn.commit()


def criar_usuario_suporte_padrao(conn):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM usuarios
        WHERE email = ?
    """, ("suporte@fitcenter.com",))

    usuario = cursor.fetchone()

    if not usuario:

        cursor.execute("""
        INSERT INTO usuarios
        (nome, email, senha, perfil)
        VALUES (?, ?, ?, ?)
        """, (
            "Suporte FitCenter",
            "suporte@fitcenter.com",
            "123456",
            "suporte"
        ))

        conn.commit()