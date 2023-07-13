import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlite_file_name = "../database.sqlite"

base_dir = os.path.dirname(os.path.realpath(__file__))

database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

#echo=True used to show in console the process of DB creation
engine = create_engine(database_url, echo=True)

#Session to connect to DB
Session = sessionmaker(bind=engine)

#Creates a base class, that other classes will inherit from, to represent tables
Base = declarative_base()