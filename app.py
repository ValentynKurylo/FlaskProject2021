from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import DATABASE_URI
from models import Base,  Worker
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from flask_marshmallow import Marshmallow
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World! - 15'



db = SQLAlchemy(app)
engine = create_engine(DATABASE_URI)
ma = Marshmallow(engine)
Session = sessionmaker(bind=engine)
s = Session()
bcrypt = flask.ext.bcrypt.Bcrypt(app)

@app.route('/worker', methods=['POST'])
def addWorker():
    name = request.json['name']
    login = request.json['login']
    password = request.json['password']
    pw_hash = bcrypt.generate_password_hash(password)
    role = request.json['role']

    new_worker = Worker(name, login, pw_hash, role)
    db.session.add(new_worker)
    db.session.comit()

    return Worker.jsonify(new_worker)
if __name__ == '__main__':
    app.run()


#alembic stamp head
#alembic revision --autogenerate
#alembic upgrade head