from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.db_config import SettingsTemporalDB, SettingsDB

# Config DataBase
config_instance = SettingsTemporalDB()

print(f"*** Ruta de la base de datos \n - {config_instance.SQLALCHEMY_DATABASE_URI}")

engine = create_engine(
    config_instance.SQLALCHEMY_DATABASE_URI , connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()