# biblioteca/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base
import datetime

# --- MODELOS SIN HERENCIA (Socio se añade aquí) ---


class Autor(Base):
    __tablename__ = 'autores'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    libros = relationship("Libro", back_populates="autor")

    def __repr__(self):
        return f"<Autor(nombre='{self.nombre}')>"


class Genero(Base):
    __tablename__ = 'generos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False, unique=True)
    libros = relationship("Libro", back_populates="genero")

    def __repr__(self):
        return f"<Genero(nombre='{self.nombre}')>"


class Socio(Base):
    __tablename__ = 'socios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    # Un socio puede tener muchos préstamos
    prestamos = relationship("Prestamo", back_populates="socio")

    def __repr__(self):
        return f"<Socio(nombre='{self.nombre} {self.apellido}')>"


# --- MODELOS CON HERENCIA (ItemBiblioteca se modifica) ---

class ItemBiblioteca(Base):
    __tablename__ = 'items_biblioteca'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    año_publicacion = Column(Integer)

    estado = Column(String(20), nullable=False, default='disponible')

    tipo = Column(String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'item_biblioteca',
        'polymorphic_on': tipo
    }

    def __repr__(self):
        return f"<Item(titulo='{self.titulo}', estado='{self.estado}')>"


class Libro(ItemBiblioteca):

    __tablename__ = 'libros'
    id = Column(Integer, ForeignKey('items_biblioteca.id'), primary_key=True)
    autor_id = Column(Integer, ForeignKey('autores.id'))
    genero_id = Column(Integer, ForeignKey('generos.id'))
    autor = relationship("Autor", back_populates="libros")
    genero = relationship("Genero", back_populates="libros")
    __mapper_args__ = {'polymorphic_identity': 'libro'}

    def __repr__(self):
        return f"<Libro(titulo='{self.titulo}', autor='{self.autor.nombre if self.autor else 'N/A'}', estado='{self.estado}')>"


class Revista(ItemBiblioteca):

    __tablename__ = 'revistas'
    id = Column(Integer, ForeignKey('items_biblioteca.id'), primary_key=True)
    editorial = Column(String(100))
    numero = Column(Integer)
    __mapper_args__ = {'polymorphic_identity': 'revista'}

    def __repr__(self):
        return f"<Revista(titulo='{self.titulo}', numero={self.numero}, estado='{self.estado}')>"


# Esta es una tabla de asociación que conecta un Socio con un ItemBiblioteca
class Prestamo(Base):
    __tablename__ = 'prestamos'
    id = Column(Integer, primary_key=True)

    # Relaciones
    item_id = Column(Integer, ForeignKey(
        'items_biblioteca.id'), nullable=False)
    socio_id = Column(Integer, ForeignKey('socios.id'), nullable=False)

    # Fechas
    fecha_prestamo = Column(Date, nullable=False, default=datetime.date.today)
    # Es NULO si aún no se ha devuelto
    fecha_devolucion = Column(Date, nullable=True)

    # Conexiones a nivel de objeto
    socio = relationship("Socio", back_populates="prestamos")
    item = relationship("ItemBiblioteca")

    def __repr__(self):
        devuelto = f"devuelto el {self.fecha_devolucion}" if self.fecha_devolucion else "aún prestado"
        return f"<Prestamo(item='{self.item.titulo}', socio='{self.socio.nombre}', {devuelto})>"
