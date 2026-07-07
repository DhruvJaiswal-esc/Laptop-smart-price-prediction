from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
import os
# =====================================================
# DATABASE CONFIGURATION
# =====================================================

import os

DATABASE_USERNAME = "postgres"

DATABASE_PASSWORD = "Firena123"

DATABASE_HOST = "localhost"

DATABASE_PORT = "5432"

DATABASE_NAME = "LaptopMarketIntelligence"

DATABASE_URL = os.getenv(

    "DATABASE_URL",

    f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

)
# =====================================================
# SQLALCHEMY ENGINE
# =====================================================

engine = create_engine(

    DATABASE_URL,

    echo=False,

    future=True

)

# =====================================================
# SESSION
# =====================================================

SessionLocal = sessionmaker(

    bind=engine,

    autoflush=False,

    autocommit=False,

    future=True

)

# =====================================================
# BASE CLASS
# =====================================================

class Base(DeclarativeBase):

    pass

# =====================================================
# FASTAPI DATABASE DEPENDENCY
# =====================================================

def get_db():

    db: Session = SessionLocal()

    try:

        yield db

    finally:

        db.close()

# =====================================================
# CREATE TABLES
# =====================================================

def create_database():

    print("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    print("Database tables ready.")

# =====================================================
# CONNECTION TEST
# =====================================================

def test_connection():

    try:

        with engine.connect() as connection:

            print("\n===================================")

            print(" PostgreSQL Connected Successfully ")

            print("===================================\n")

            return True

    except Exception as e:

        print("\n===================================")

        print(" Database Connection Failed ")

        print("===================================\n")

        print(e)

        return False

# =====================================================
# RUN DIRECTLY
# =====================================================

if __name__ == "__main__":

    test_connection()