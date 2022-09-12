
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
# from app.settings.configurations.config import Settings
import pyodbc


# settings = Settings()

# if settings.DEBUG:
#     connection_string = settings.DEVELOPMENT_DATABASE_URL
# else:
#     connection_string = settings.PRODUCTION_DATABASE_URL

connection_string = "DRIVER={SQL Server};SERVER=172.16.2.64;DATABASE=ImageQcDbTest;UID=imageqcuser;PWD=Password1"

connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})


engine = create_engine(connection_url)
con = engine.connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



