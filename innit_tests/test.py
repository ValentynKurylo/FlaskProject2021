import unittest
from sqlalchemy.orm import sessionmaker
import unittest

from app import app, Session
from base64 import b64encode
import json
from models import Base, User, engine,  Product
from user import bcrypt



class TestingBase(unittest.TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    tester = app.test_client()
    session = Session()

    def tearDown(self):
        self.close_session()

    def close_session(self):
        self.session.close()




class ApiTest(TestingBase):
    user = {
        "name": "ValentynKurylo",
        "login": "barany1818@gmail.com",
        "password": "12345678",
        "role": "admin"
    }

    products = {
        "name": "tabletky",
        "price": 20,
        "number": 5

    }


    def test_User_Creation(self):
        response = self.tester.post("/users/", data=json.dumps(self.user), content_type="application/json")
        print(response.data)
        code = response.status_code
        self.assertEqual(200, code)
        self.session.query(User).filter_by(name='ValentynKurylo').delete()
        self.session.commit()

    def test_User_Creation_invalid(self):
        response = self.tester.post("/users/", data=json.dumps({
            "name": "Valentyn_Kurylo2",
            "login": "barany2@gmail.com",
            "password": "12345678",
            "role": "user"
    }), content_type="application/json")
        code = response.status_code
        self.assertEqual(400, code)

    def test_Get_User(self):

        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(id=1233, name="ValentynKurylo", login="barany116@gmail.com", password=hashpassword, role="worker")
        self.session.add(user)
        self.session.commit()
        response = self.tester.get('/users')
        self.session.delete(user)
        self.session.commit()
        code = response.status_code
        self.assertEqual(200, code)


    def test_Update_User(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="SoniaPlaystation", login="baranya@gmail.com",  password=hashpassword, role="user")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"cucumber@gmail.com:12345678").decode("utf-8")
        response = self.tester.put('/users/1',
                                   data=json.dumps({"nickname": "Sonya", "login": "baranyyy@gmail.com",
                                                    "password": "12345678", "role": "user"}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)
        self.session.query(User).filter_by(name='Sonya').delete()
        self.session.commit()

    def test_Update_User_invalid(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="SoniaPlaystation", login="baranya@gmail.com", password=hashpassword, role="user")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"SoniaPlaystation:12345678").decode("utf-8")
        response = self.tester.put('/users/1',
                                   data=json.dumps({"nickname": "Sonya", "login": "baranyyy@gmail.com",
                                                    "password": "12345678", "role": "user"}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(400, code)
        self.session.query(User).filter_by(name='SoniaPlaystation').delete()
        self.session.commit()

    def test_Delete_User_by_Id(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="SoniaPlaystatio", login="bara@gmail.com", password=hashpassword, role="user")
        self.session.add(user)
        self.session.commit()
        # creds = b64encode(b"SoniaPlaystati:12345678").decode("utf-8")
        response = self.tester.delete('/users/124')
        code = response.status_code
        self.assertEqual(401, code)

    def test_Login_User(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="baran@gmail.com", password=hashpassword, role="user")
        self.session.add(user)
        self.session.commit()
        response = self.tester.get('/users/login', data=json.dumps({"name": "rassel", "password": "12345678"}),
                                   content_type="application/json")
        self.session.delete(user)
        self.session.commit()
        code = response.status_code
        self.assertEqual(200, code)

    def test_Login_User_invalid1(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="user")
        self.session.add(user)
        self.session.commit()
        response = self.tester.get('/users/login', data=json.dumps({"nickname": "rasssel", "password": "12345678"}),
                                   content_type="application/json")
        self.session.delete(user)
        self.session.commit()
        code = response.status_code
        self.assertEqual(400, code)

    def test_Login_User_invalid2(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="user")
        self.session.add(user)
        self.session.commit()
        response = self.tester.get('/users/login', data=json.dumps({"nickname": "rassel", "password": "5678"}),
                                   content_type="application/json")
        self.session.delete(user)
        self.session.commit()
        code = response.status_code
        self.assertEqual(400, code)

    def test_Create_Product(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="worker")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"tomato@gmail.com:12345678").decode("utf-8")
        response = self.tester.post("/products/", data=json.dumps(self.products),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)
        self.session.query(Product).filter_by(name='Cytramon').delete()
        self.session.query(User).filter_by(name='rassel').delete()
        self.session.commit()


    def test_Delete_Product_by_Id(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="worker")
        drug = Product(name="aspiryn", price=10, number=5)
        self.session.add(drug)
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"tomato@gmail.com:12345678").decode("utf-8")
        response = self.tester.delete('/products/1', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(401, code)
        self.session.delete(user)
        self.session.commit()


    def test_Create_Product_Invalid(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="user")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"tomato@gmail.com:12345678").decode("utf-8")
        response = self.tester.post("/products/", data=json.dumps(self.products),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(400, code)
        self.session.query(Product).filter_by(name='Cytramon').delete()
        self.session.query(User).filter_by(name='rassel').delete()
        self.session.commit()


    def test_Delete_Product_by_Id(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="worker")
        drug = Product(name="aspiryn", price=10, number=5)
        self.session.add(drug)
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"tomato@gmail.com:12345678").decode("utf-8")
        response = self.tester.delete('/products/1', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)
        self.session.delete(user)
        self.session.commit()

    def test_Delete_Product_by_Id_Invali(self):
        hashpassword = bcrypt.generate_password_hash('12345678')
        user = User(name="rassel", login="tomato@gmail.com", password=hashpassword, role="worker")
        drug = Product(name="aspiryn", price=10, number=5)
        self.session.add(drug)
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"tomato@gmail.com:12345678").decode("utf-8")
        response = self.tester.delete('/products/10', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(400, code)
        self.session.delete(user)
        self.session.commit()
