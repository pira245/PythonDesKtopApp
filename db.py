from sqlalchemy import Table, Column, Integer, Numeric, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select

#For relationship between tables
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey, Boolean

#For Database clases and metadata mapping
Base = declarative_base()
from sqlalchemy import create_engine

#For database creation
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///database/productos.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()



