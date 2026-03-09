from flask import Flask, send_from_directory
import os

# ===============================
# BANCO DE DADOS
# ===============================

from database.database import conectar, criar_usuario_padrao

# ===============================
# ROTAS DO SISTEMA
# ===============================

from routes.dashboard_routes import dashboard_bp
from routes.aluno_routes import aluno_bp
from routes.aluno_portal_routes import aluno_portal_bp
from routes.auth_routes import auth_bp
from routes.treinador_routes import treinador_bp
from routes.treino_routes import treino_bp
from routes.nutri_routes import nutri_bp
from routes.exercicios_routes import exercicios_bp
from routes.avaliacao_routes import avaliacao_bp
from routes.admin_routes import admin_bp


# ===============================
# INICIALIZAÇÃO DO APP
# ===============================

app = Flask(__name__)

app.secret_key = "fitcenter_secret"


# ===============================
# PASTAS DE UPLOAD
# ===============================

UPLOAD_TREINOS = "uploads/treinos"
UPLOAD_DIETAS = "uploads/dietas"
UPLOAD_AVALIACOES = "uploads/avaliacoes"

os.makedirs(UPLOAD_TREINOS, exist_ok=True)
os.makedirs(UPLOAD_DIETAS, exist_ok=True)
os.makedirs(UPLOAD_AVALIACOES, exist_ok=True)


# ===============================
# GARANTIR QUE O BANCO EXISTE
# ===============================

def iniciar_banco():

    conn = conectar()
    conn.close()


iniciar_banco()


# ===============================
# CRIAR USUÁRIO PADRÃO DO SISTEMA
# ===============================

criar_usuario_padrao()


# ===============================
# REGISTRAR BLUEPRINTS
# ===============================

blueprints = [

    dashboard_bp,
    aluno_bp,
    aluno_portal_bp,
    auth_bp,
    treinador_bp,
    treino_bp,
    nutri_bp,
    exercicios_bp,
    avaliacao_bp,
    admin_bp

]

for bp in blueprints:
    app.register_blueprint(bp)


# ===============================
# ROTAS PARA ACESSAR ARQUIVOS
# ===============================

@app.route("/uploads/treinos/<filename>")
def ver_treino(filename):

    return send_from_directory(UPLOAD_TREINOS, filename)


@app.route("/uploads/dietas/<filename>")
def ver_dieta(filename):

    return send_from_directory(UPLOAD_DIETAS, filename)


@app.route("/uploads/avaliacoes/<filename>")
def ver_avaliacao(filename):

    return send_from_directory(UPLOAD_AVALIACOES, filename)


# ===============================
# INICIAR SERVIDOR
# ===============================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )