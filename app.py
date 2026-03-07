from flask import Flask

# banco
from database.database import criar_banco

# rotas
from routes.dashboard_routes import dashboard_bp
from routes.aluno_routes import aluno_bp
from routes.aluno_portal_routes import aluno_portal_bp
from routes.auth_routes import auth_bp
from routes.treinador_routes import treinador_bp
from routes.treino_routes import treino_bp
from routes.nutri_routes import nutri_bp


app = Flask(__name__)

app.secret_key = "fitcenter_secret"


# cria banco automaticamente
criar_banco()


# registrar rotas
app.register_blueprint(dashboard_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(aluno_portal_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(treinador_bp)
app.register_blueprint(treino_bp)
app.register_blueprint(nutri_bp)


# iniciar sistema
if __name__ == "__main__":
    app.run(debug=True)