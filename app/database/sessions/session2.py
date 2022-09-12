
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from app.core.settings.config import AppSettings
import pyodbc


settings = AppSettings()


connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=172.16.2.64;DATABASE=CardGenDb;UID=imageprocessuser;PWD=Password1"

connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})


engine2 = create_engine(connection_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine2)

Base2 =  declarative_base()

