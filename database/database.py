import sqlite3


def conectar():
    conn = sqlite3.connect("fitcenter.db")
    conn.row_factory = sqlite3.Row
    return conn


def criar_banco():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        apelido TEXT,
        email TEXT UNIQUE,
        senha TEXT,
        tipo TEXT,
        foto TEXT

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        apelido TEXT,
        email TEXT UNIQUE,
        senha TEXT,
        genero TEXT,
        foto TEXT,
        xp INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercicios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        nome TEXT,
        series INTEGER,
        repeticoes INTEGER,
        peso INTEGER

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico_treino (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        exercicio TEXT,
        peso INTEGER,
        repeticoes INTEGER,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()