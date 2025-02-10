from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pyodbc


server_PROD = "localhost"
database_PROD = "innoveo"
username_PROD = "sa"
password_PROD = "12345"
driver = 'ODBC Driver 18 for SQL Server'


# Construindo a string de conexão
SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://{username_PROD}:{password_PROD}@{server_PROD}/{database_PROD}?driver={driver}&Encrypt=no"
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/innoveo"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
#engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def abrir_sessao_sql_server():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    return engine , SessionLocal ,Base