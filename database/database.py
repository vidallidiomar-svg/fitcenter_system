import sqlite3


def conectar():

    conn = sqlite3.connect("fitcenter.db")
    conn.row_factory = sqlite3.Row

    return conn


def criar_banco():

    conn = conectar()
    cursor = conn.cursor()


    # ================================
    # USUÁRIOS DO SISTEMA
    # ================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS usuarios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT UNIQUE,
        senha TEXT,
        tipo TEXT,
        foto TEXT

    )

    """)


    # ================================
    # ALUNOS
    # ================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS alunos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        apelido TEXT,
        email TEXT,
        genero TEXT,
        xp INTEGER,
        streak INTEGER,
        foto TEXT

    )

    """)


    # ================================
    # TREINOS
    # ================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS treinos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        nome TEXT,
        data TEXT

    )

    """)


    # ================================
    # EXERCÍCIOS
    # ================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS exercicios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        grupo_muscular TEXT

    )

    """)


    # ================================
    # TREINO_EXERCICIOS
    # ================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS treino_exercicios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        treino_id INTEGER,
        exercicio_id INTEGER,

        ordem INTEGER,

        series INTEGER,
        repeticoes TEXT,

        peso TEXT,

        intervalo INTEGER,

        metodo TEXT,

        movimento TEXT,

        observacoes TEXT

    )

    """)


    conn.commit()
    conn.close()