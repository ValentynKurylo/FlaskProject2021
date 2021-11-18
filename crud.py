from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import DATABASE_URI
from models import Base,  Worker
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
engine = create_engine(DATABASE_URI)
'''
app = Flask(__name__)
db = SQLAlchemy(app)
engine = create_engine(DATABASE_URI)
ma = Marshmallow(engine)
Session = sessionmaker(bind=engine)
s = Session()
bcrypt = Bcrypt(app)

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

    return Worker.jsonify(new_worker)'''
'''
worker1 = Worker(
        name='Valentyn Kurylo',
        login='Kurylo@gmail',
        password='kurylo',
        role='admin'

    )
s.add(worker1)
s.comit()
s.close()


ma = Marshmallow(engine)
#s = Session()


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


#def load_yaml():
   #with session_scope() as s:
       #for data in yaml.load_all(open('students.yaml')):
           #student = Student(**data)
           #s.add(student)


if __name__ == '__main__':
    worker = Worker(
        id=1,
        name='Valentyn Kurylo',
        login='Kurylo@gmail',
        password='kurylo',
        role='admin'

    )
    with session_scope() as s:
        s.add(worker)
        '''
