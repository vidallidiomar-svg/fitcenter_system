import sqlite3


def conectar():

    conn = sqlite3.connect("fitcenter.db")
    conn.row_factory = sqlite3.Row

    return conn


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
        genero TEXT,
        xp INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercicios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        exercicio TEXT,
        series INTEGER,
        repeticoes INTEGER,
        peso TEXT,
        concluido INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico_treino(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        exercicio TEXT,
        peso INTEGER,
        data TEXT
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
    conn.close()