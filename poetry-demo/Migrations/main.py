# coding=utf-8

from sqlalchemy import Integer, String, Column, ForeignKey

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

# mysql+pymysql://root:EL_PRESIDENTO@localhost:3306/cash
engine = create_engine('mysql+pymysql://root:12345678@127.0.0.1:3306/forppproject')

SessionFactory = sessionmaker(bind=engine)

Session = scoped_session(SessionFactory)

Base = declarative_base()
metadata = Base.metadata

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
    fr0m_id = Column(Integer, ForeignKey('wallet.id'), nullable=False)
    to_id = Column(Integer, ForeignKey('wallet.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    fr0m = relationship("Wallet", foreign_keys=[fr0m_id])
    to = relationship("Wallet", foreign_keys=[to_id])


class Wallet(Base):
    __tablename__ = 'wallet'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    amount = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship("User")
