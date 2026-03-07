import sqlite3


def conectar():

    conn = sqlite3.connect("fitcenter.db")
    conn.row_factory = sqlite3.Row

    criar_tabelas(conn)

    return conn


def criar_tabelas(conn):

    cursor = conn.cursor()

    # =========================
    # TABELA ALUNOS
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        apelido TEXT,
        email TEXT,
        senha TEXT,
        genero TEXT,
        foto TEXT,
        xp INTEGER DEFAULT 0

    )
    """)

    # =========================
    # TABELA TREINOS
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treinos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        nome TEXT

    )
    """)

    # =========================
    # TABELA EXERCICIOS
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treino_exercicios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        treino_id INTEGER,
        ordem INTEGER,
        nome TEXT,
        series TEXT,
        repeticoes TEXT,
        peso TEXT,
        intervalo TEXT,
        metodo TEXT,
        movimento TEXT

    )
    """)

    conn.commit()