import sqlite3

def criar_banco():

    conn = sqlite3.connect("fitcenter.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treinos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        descricao TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avaliacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        peso REAL,
        gordura REAL,
        massa_muscular REAL,
        data TEXT
    )
    """)

    conn.commit()
    conn.close()

