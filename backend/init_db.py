"""
Script to initialize the database with sample data
Run this once to populate the database
"""

from database import create_db_and_tables, engine
from models import Contest
from sqlmodel import Session

def init_db():
    """Initialize database with sample data"""
    create_db_and_tables()
    
    with Session(engine) as session:
        # Check if data already exists
        from sqlmodel import select
        existing = session.exec(select(Contest)).first()
        if existing:
            print("Database already populated!")
            return
if __name__ == "__main__":
    init_db()
