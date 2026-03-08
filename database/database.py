import sqlite3


# ===============================
# CONEXÃO COM O BANCO
# ===============================

def conectar():

    conn = sqlite3.connect("fitcenter.db")
    conn.row_factory = sqlite3.Row

    criar_tabelas(conn)

    return conn


# ===============================
# CRIAR TABELAS
# ===============================

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
        xp INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0

    )

    """)


    # =========================
    # TABELA USUÁRIOS (LOGIN)
    # =========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS usuarios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT,
        senha TEXT,
        perfil TEXT

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
    # TABELA EXERCÍCIOS DO TREINO
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

        peso_real TEXT,
        reps_real TEXT,
        concluido INTEGER DEFAULT 0

    )

    """)


    # =========================
    # TABELA AVALIAÇÕES FÍSICAS
    # =========================

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


    # =========================
    # BIBLIOTECA DE EXERCÍCIOS
    # =========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS exercicios (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        grupo TEXT,
        equipamento TEXT

    )

    """)


    # =========================
    # PLANOS ALIMENTARES
    # =========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS planos (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER,
        nome TEXT

    )

    """)


    # =========================
    # REFEIÇÕES DO PLANO
    # =========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS refeicoes (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plano_id INTEGER,
        refeicao TEXT,
        alimento TEXT,
        quantidade TEXT,
        calorias INTEGER,
        proteina INTEGER,
        carbo INTEGER,
        gordura INTEGER

    )

    """)


    conn.commit()