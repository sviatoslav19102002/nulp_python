import unittest
from app import app
from base64 import b64encode
import json
from Migrations.main import User, Wallet, Transfer, engine, Base, Session

class TestingBase(unittest.TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    tester = app.test_client()
    session = Session()

    def setUp(self):
        delete()

    def tearDown(self):
        self.close_session()

    def close_session(self):
        self.session.close()

class ApiTest(TestingBase):
    user1 = {
        "username": "slayer",
        "password": "123456",
        "email": "slayer666@gmail.com",
        "first_name": "Stepan",
        "second_name": "Stepanenko"
    }
    user2 = {
        "username": "slayer2",
        "password": "123456",
        "email": "slayer666(2)@gmail.com",
        "first_name": "Stepan2",
        "second_name": "Stepanenko2"
    }
    user3 = {
        "username": "slayer2",
        "password": "12345",
        "email": "slayer666(2)@gmail.com",
        "first_name": "Stepan2",
        "second_name": "Stepanenko2"
    }
    wallet1 = {
        "name": "wallet1",
        "amount": 10000,
        "owner_id": 1
    }
    wallet2 = {
        "name": "wallet2",
        "amount": 5000,
        "owner_id": 2
    }
    transfer1 = {
        "purpose": "Salary",
        "fr0m_id": 1,
        "to_id": 2,
        "amount": 5000
    }
    transfer2 = {
        "purpose": "Debt",
        "fr0m_id": 3,
        "to_id": 1,
        "amount": 500
    }


    def test_register_user(self):
        delete()
        response = self.tester.post("/api/v1/auth/register", data=json.dumps(self.user1),
                                    content_type="application/json")
        code = response.status_code
        self.assertEqual(200, code)

    def test_register_user_wrong_1(self):
        delete()
        response = self.tester.post("/api/v1/auth/register", data=json.dumps(self.user3),
                                    content_type="application/json")
        code = response.status_code
        self.assertEqual(401, code)

    def test_get_user_by_username(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer", password="123456")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.get('/api/v1/user/slayer', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)
        self.assertEqual({
            "user": {
                "email": "salabay2003@gmail.com",
                "first_name": "Bohdan",
                "id": 1,
                "second_name": "Salabay",
                "username": "slayer"
            }
        }, response.json)

    def test_get_user_by_username_wrong(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer", password="123456")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.get('/api/v1/user/slayer2', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(406, code)

    def test_update_user(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer", password="123456")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.put('/api/v1/user/slayer',
                                   data=json.dumps({"username": "slayer1", "first_name": "Bohdan1", "second_name": "Salabay1",
                                                    "password": "12345678"}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_update_user_1(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer", password="123456")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.put('/api/v1/user/slayer',
                                   data=json.dumps({"username": "slayer1", "first_name": "Bohdan1", "second_name": "Salabay1",
                                                    "password": "12345"}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(400, code)

    def test_update_user_2(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer", password="123456")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.put('/api/v1/user/slayer2',
                                   data=json.dumps({"username": "slayer1", "first_name": "Bohdan1", "second_name": "Salabay1",
                                                    "password": "12345678"}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(406, code)

    def test_delete_user_by_username(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer", password="123456")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.delete('/api/v1/user/slayer', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_delete_user_by_username_1(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer", password="123456")
        user2 = User(id=2, first_name="Bohdan2", second_name="Salabay2", email="salabay20032@gmail.com", username="slayer2", password="123456")
        self.session.add(user)
        self.session.add(user2)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.delete('/api/v1/user/slayer2', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(406, code)


    def test_create_wallet(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer",
                    password="123456")
        self.session.add(user)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.post("/api/v1/wallet", data=json.dumps(self.wallet1),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_create_wallet_wrong_1(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer",
                    password="123456")
        wallet = Wallet(id=1, name="wallet1", amount=10000, owner_id=1)
        self.session.add(user)
        self.session.add(wallet)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.post("/api/v1/wallet", data=json.dumps(self.wallet1),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(400, code)

    def test_create_wallet_wrong_2(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer",
                    password="123456")
        self.session.add(user)
        self.session.commit()
        wallet1 = {
            "name": "wallet1",
            "amount": 10000,
            "owner_id": 2
        }
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.post("/api/v1/wallet", data=json.dumps(wallet1),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(406, code)

    def test_get_wallet_by_name(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer", password="123456")
        self.session.add(user)
        wallet = Wallet(id=1, name="wallet1", amount=10000, owner_id=1)
        self.session.add(wallet)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.get('/api/v1/wallet/wallet1', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_get_wallet_by_name_wrong_1(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer", password="123456")
        self.session.add(user)
        wallet = Wallet(id=1, name="wallet1", amount=10000, owner_id=1)
        self.session.add(wallet)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.get('/api/v1/wallet/wallet2', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_get_wallet_by_name_wrong_2(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer", password="123456")
        user2 = User(id=2, first_name="Bohdan", second_name="Salabay", email="salabay20032@gmail.com", username="slayer2",
                    password="123456")
        self.session.add(user)
        self.session.add(user2)
        wallet = Wallet(id=1, name="wallet1", amount=10000, owner_id=1)
        self.session.add(wallet)
        self.session.commit()
        creds = b64encode(b"slayer2:123456").decode("utf-8")
        response = self.tester.get('/api/v1/wallet/wallet1', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(406, code)


    def test_update_wallet(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer", password="123456")
        self.session.add(user)
        wallet = Wallet(id=1, name="wallet1", amount=10000, owner_id=1)
        self.session.add(wallet)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.put('/api/v1/wallet/wallet1',
                                   data=json.dumps({"name": "wallet", "amount": 10000, "owner_id": 1}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_update_wallet_1(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer",
                    password="123456")
        self.session.add(user)
        wallet = Wallet(id=1, name="wallet1", amount=10000, owner_id=1)
        self.session.add(wallet)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.put('/api/v1/wallet/wallet2',
                                   data=json.dumps({"name": "wallet", "amount": 10000, "owner_id": 1}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_update_wallet_2(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer",
                    password="123456")
        self.session.add(user)
        wallet = Wallet(id=1, name="wallet1", amount=10000, owner_id=1)
        self.session.add(wallet)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.put('/api/v1/wallet/wallet1',
                                   data=json.dumps({"name": "wallet", "amount": 10000, "owner_id": 2}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(406, code)

    def test_update_wallet_3(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer",
                    password="123456")
        self.session.add(user)
        wallet = Wallet(id=1, name="wallet1", amount=10000, owner_id=1)
        self.session.add(wallet)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.put('/api/v1/wallet/wallet1',
                                   data=json.dumps({"name": "wa", "amount": 10000, "owner_id": 1}),
                                   content_type='application/json', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(400, code)

    def test_delete_wallet_by_name(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer",
                    password="123456")
        self.session.add(user)
        wallet = Wallet(id=1, name="wallet1", amount=10000, owner_id=1)
        self.session.add(wallet)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.delete('/api/v1/wallet/wallet1', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_delete_wallet_by_name_1(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer",
                    password="123456")
        self.session.add(user)
        wallet = Wallet(id=1, name="wallet1", amount=10000, owner_id=1)
        self.session.add(wallet)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.delete('/api/v1/wallet/wallet11', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(404, code)

    def test_delete_wallet_by_name_2(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer",
                    password="123456")
        user2 = User(id=2, first_name="Bohdan", second_name="Salabay", email="salabay20032@gmail.com", username="slayer2",
                    password="123456")
        self.session.add(user)
        self.session.add(user2)
        wallet = Wallet(id=1, name="wallet1", amount=10000, owner_id=2)
        self.session.add(wallet)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.delete('/api/v1/wallet/wallet1', headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(406, code)


    def test_create_transfer(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer",
                    password="123456")
        user2 = User(id=2, first_name="Bohdan", second_name="Salabay", email="salabay20032@gmail.com",
                     username="slayer2",
                     password="123456")
        self.session.add(user)
        self.session.add(user2)
        wallet1 = Wallet(id=1, name="wallet1", amount=10000, owner_id=1)
        wallet2 = Wallet(id=2, name="wallet2", amount=500, owner_id=2)
        self.session.add(wallet1)
        self.session.add(wallet2)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.post("/api/v1/transfer", data=json.dumps(self.transfer1),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(200, code)

    def test_create_transfer_wrong(self):
        delete()
        user = User(id=1, first_name="Bohdan", second_name="Salabay", email="salabay2003@gmail.com", username="slayer",
                    password="123456")
        user2 = User(id=2, first_name="Bohdan", second_name="Salabay", email="salabay20032@gmail.com",
                     username="slayer2",
                     password="123456")
        self.session.add(user)
        self.session.add(user2)
        wallet1 = Wallet(id=1, name="wallet1", amount=1000000, owner_id=1)
        wallet2 = Wallet(id=2, name="wallet2", amount=500, owner_id=2)
        self.session.add(wallet1)
        self.session.add(wallet2)
        self.session.commit()
        creds = b64encode(b"slayer:123456").decode("utf-8")
        response = self.tester.post("/api/v1/transfer", data=json.dumps(self.transfer2),
                                    content_type="application/json", headers={"Authorization": f"Basic {creds}"})
        code = response.status_code
        self.assertEqual(400, code)


def delete():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    unittest.main()