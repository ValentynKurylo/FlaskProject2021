
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from config import DATABASE_URI
from flask_migrate import Migrate
from worker import worker
from user import user
from product import product
from order import order
from productDemand import productDemand

app = Flask(__name__)

db = SQLAlchemy()
engine = create_engine(DATABASE_URI)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kurylo13@localhost:5432/pharmacy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ma = Marshmallow(engine)
Session = sessionmaker(bind=engine)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
app.register_blueprint(worker)
app.register_blueprint(user)
app.register_blueprint(product)
app.register_blueprint(order)
app.register_blueprint(productDemand)

@app.route('/')
def hello_world():
    return 'Hello World! - 15'



if __name__ == '__main__':
    app.run(debung=True)



#alembic stamp head
#alembic revision --autogenerate
#alembic upgrade head
