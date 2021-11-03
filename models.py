from sqlalchemy import Column, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    name = Column(String(45), nullable=False)
    username = Column(String(45))
    password = Column(String(45))


class Tickets(Base):
    __tablename__ = "Tickets"
    id = Column(Integer, primary_key=True)
    row = Column(Integer)
    place = Column(Integer)
    namefilm = Column(String(45))
    datatime = Column(DATETIME)
    reservation = Column(String(45))
    buy = Column(String(45))


class Buy(Base):
    __tablename__ = "Buy"
    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    idticket = Column(Integer, ForeignKey('Tickets.id'))
    tickets = relationship("Tickets")

