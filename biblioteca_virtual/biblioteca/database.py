# biblioteca/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL
# Creamos el motor que se conectará a la base de datos
engine = create_engine(DATABASE_URL)

# Creamos una fábrica de sesiones para crear sesiones de trabajo con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creamos una clase Base de la que heredarán nuestros modelos
Base = declarative_base()


def init_db():
    """Función para crear todas las tablas en la base de datos."""
    print("Creando tablas en la base de datos si no existen...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas/verificadas con éxito.")
