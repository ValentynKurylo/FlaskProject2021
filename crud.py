from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import DATABASE_URI
from models import Base,  Worker
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

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
