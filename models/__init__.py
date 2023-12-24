from config.database import SessionLocal, engine
from sqlalchemy.orm import declarative_base

class DatabaseManager():
    def __init__(self):
        self.session_maker = SessionLocal
        self.session = self.session_maker()
        self.engine = engine
        self.base = declarative_base()

db = DatabaseManager()