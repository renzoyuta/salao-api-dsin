import os

from database.connection import db
from database.seed import seed_agendamentos, seed_clientes, seed_servicos
from flask import Flask
from models.agendamento import Agendamento  # noqa: F401
from models.cliente import Cliente  # noqa: F401
from models.servico import Servico  # noqa: F401
from routes.agendamento_routes import agendamento_bp
from routes.cliente_routes import cliente_bp
from routes.servico_routes import servico_bp

app = Flask(__name__)

BACKEND_DIR = os.path.abspath(os.path.dirname(__file__))

database_path = os.path.join(BACKEND_DIR, "database/salao.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(agendamento_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(servico_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_clientes()
        seed_servicos()
        seed_agendamentos()

    app.run(debug=True)
