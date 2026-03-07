from flask import Flask
from database.database import criar_banco

from routes.auth_routes import auth_bp
from routes.aluno_routes import aluno_bp
from routes.treino_routes import treino_bp
from routes.dashboard_routes import dashboard_bp

app = Flask(__name__)
app.secret_key = "fitcenter_secret"

criar_banco()

app.register_blueprint(auth_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(treino_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(debug=True)