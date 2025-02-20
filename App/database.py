# database.py (updated)
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Base, Product

# Global engine and session factory for efficiency
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def get_db_session():
    return SessionLocal()

def get_all_products():
    session = get_db_session()
    results = session.query(Product).all()
    session.close()
    return results

def get_product_count_and_max_id():
    session = get_db_session()
    count = session.query(func.count(Product.id)).scalar()
    max_id = session.query(func.max(Product.id)).scalar()
    session.close()
    return count, max_id

def get_new_products(last_max_id):
    session = get_db_session()
    new_products = session.query(Product).filter(Product.id > last_max_id).all()
    session.close()
    return new_products