# models.py
from sqlalchemy import Column, Integer, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'shahzar_table'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    image = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    store = Column(Text, nullable=False)