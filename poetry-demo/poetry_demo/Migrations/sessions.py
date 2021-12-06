from main import Wallet, Transfer, User, Session


s = Session()

user = User(id = 1, username ="warior", password="123456789",
            email="price@gmail.com",first_name="John",second_name="Price")
user1 = User(id=2, username="president", password="123456789",
             email="underwood@gmail.com",first_name="Francic",second_name="Underwood")

wallet = Wallet(id=1, name="DutyWallet", amount=1000000, owner_id=1)
wallet1 = Wallet(id=2,name="WhiteHouseWallet", amount=50000000, owner_id=2)

transfer = Transfer(id=1, purpose="War express", fr0m_id=1, to_id=1, amount= 1000000)
transfer1 = Transfer(id=2, purpose="White house express", fr0m_id=2, to_id=2, amount=50000000)

s.add(user)
s.add(user1)
s.add(wallet)
s.add(wallet1)
s.add(transfer)
s.add(transfer1)

s.commit()
s.close()

