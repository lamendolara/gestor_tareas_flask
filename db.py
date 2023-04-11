from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#La unica linea que se cambia es la siguiente:
engine = create_engine("sqlite:///database/tareas.db", connect_args={"check_same_thread":False}) # esto es solo necesario en programacion web. Porque se pueden generar varias peticiones a la vez.

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
