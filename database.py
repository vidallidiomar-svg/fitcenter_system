import sqlite3


def criar_banco():

    conn = sqlite3.connect("fitcenter.db")
    cursor = conn.cursor()

    # usuários do sistema
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        senha TEXT,
        tipo TEXT
    )
    """)

    # alunos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        xp INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0
    )
    """)

    # avaliações físicas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avaliacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        peso REAL,
        gordura REAL,
        massa REAL,
        data TEXT
    )
    """)

    # histórico de treino
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico_treino (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        exercicio TEXT,
        peso REAL,
        data TEXT
    )
    """)

    # exercícios do treino
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        nome TEXT,
        series INTEGER,
        repeticoes INTEGER,
        peso REAL
    )
    """)

    # cria usuário suporte automaticamente
    cursor.execute("""
    SELECT * FROM usuarios WHERE email='suportesuper@gmail.com'
    """)

    suporte = cursor.fetchone()

    if not suporte:

        cursor.execute("""
        INSERT INTO usuarios
        (nome,email,senha,tipo)
        VALUES
        ('Suporte','suportesuper@gmail.com','341062','suporte')
        """)

    conn.commit()
    conn.close()