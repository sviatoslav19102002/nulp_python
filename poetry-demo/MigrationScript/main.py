# coding=utf-8

from sqlalchemy import  Table, Integer, String, \
    Column,  ForeignKey
from sqlalchemy.ext.declarative import declarative_base






Base = declarative_base()

# Cтворення основних класів(таблиць)
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    first_name = Column(String(100), nullable=False)
    second_name = Column(String(100), nullable=False)


class Transfer(Base):
    __tablename__ = 'transfer'
    id = Column(Integer, primary_key=True)
    purpose = Column(String(100), nullable=False)
    fr0m = Column(Integer, nullable=False)  # Слово 'from' середовище розпізнавало як команду, тому я 'o' замінив на '0'
    to = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)


class Wallet(Base):
    __tablename__ = 'wallet'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    amount = Column(Integer, nullable=False)
    owner = Column(Integer, nullable=False)


# Створення залежностей "Багато до багатьох"(ця залежність є між всіма основними таблицями)
user_has_transfer = Table('user_has_transfer', Base.metadata,
                          Column('user_id', Integer(), ForeignKey("user.id")),
                          Column('transfer_id', Integer(), ForeignKey("transfer.id"))
                          )

user_has_wallet = Table('user_has_wallet', Base.metadata,
                        Column('user_id', Integer(), ForeignKey("user.id")),
                        Column('wallet_id', Integer(), ForeignKey("wallet.id"))
                        )

transfer_has_wallet = Table('transfer_has_wallet', Base.metadata,
                            Column('transfer_id', Integer(), ForeignKey("transfer.id")),
                            Column('wallet_id', Integer(), ForeignKey("wallet.id"))
                            )
