import sqlite3


def conectar():

    conn = sqlite3.connect("fitcenter.db")
    conn.row_factory = sqlite3.Row

    criar_tabelas(conn)
    criar_usuario_suporte(conn)

    return conn


def criar_tabelas(conn):

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT UNIQUE,
        senha TEXT,
        perfil TEXT

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        senha TEXT,
        genero TEXT,
        foto TEXT,
        xp INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treinos(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        nome TEXT,
        arquivo_pdf TEXT,
        concluido INTEGER DEFAULT 0

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS planos_alimentares(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        arquivo TEXT,
        data_envio TEXT

    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS avaliacoes(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        arquivo TEXT,
        data_envio TEXT

    )
    """)

    conn.commit()


def criar_usuario_suporte(conn):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM usuarios WHERE email=?",
        ("suportesuper@gmail.com",)
    )

    usuario = cursor.fetchone()

    if usuario:
        return

    cursor.execute("""
    INSERT INTO usuarios
    (nome,email,senha,perfil)
    VALUES (?,?,?,?)
    """,(
        "Suporte FitCenter",
        "suportesuper@gmail.com",
        "34106234",
        "suporte"
    ))

    conn.commit()