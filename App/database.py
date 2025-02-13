# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Base, Product

def get_db_session():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def get_all_products():
    session = get_db_session()
    results = session.query(Product).all()
    session.close()
    return results