# biblioteca/crud.py

from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models
import datetime


def cargar_datos_iniciales(db: Session):
    """Carga los datos iniciales si la base de datos está vacía."""
    if db.query(models.ItemBiblioteca).count() > 0:
        print("La base de datos ya contiene datos. No se realizará la carga inicial.")
        return

    print("Base de datos vacía, procediendo con la carga de datos iniciales...")
    try:
        # --- Carga de géneros y autores ---
        fantasia_epica = models.Genero(nombre="Fantasía Épica")
        fantasia_juvenil = models.Genero(nombre="Fantasía Juvenil")
        db.add_all([fantasia_epica, fantasia_juvenil])

        tolkien = models.Autor(nombre="J.R.R. Tolkien")
        rowling = models.Autor(nombre="J.K. Rowling")
        db.add_all([tolkien, rowling])

        # --- NUEVO: Carga de socios de ejemplo ---
        socio1 = models.Socio(nombre="Juan", apellido="Perez",
                              email="juan.perez@example.com")
        socio2 = models.Socio(nombre="Maria", apellido="Gomez",
                              email="maria.gomez@example.com")
        db.add_all([socio1, socio2])

        db.commit()

        # --- Cargar Libros y Revistas ---
        items_a_cargar = [
            models.Libro(titulo="La Comunidad del Anillo",
                         año_publicacion=1954, autor=tolkien, genero=fantasia_epica),
            models.Libro(titulo="Harry Potter y la piedra filosofal",
                         año_publicacion=1997, autor=rowling, genero=fantasia_juvenil),
            models.Revista(titulo="National Geographic",
                           año_publicacion=2024, editorial="NGS", numero=150),
        ]
        db.add_all(items_a_cargar)

        db.commit()
        print("Datos iniciales cargados exitosamente.")
    except Exception as e:
        print(f"Ocurrió un error durante la carga de datos: {e}")
        db.rollback()

# --- NUEVAS FUNCIONES PARA PRÉSTAMOS ---


def crear_prestamo(db: Session, socio_id: int, item_id: int) -> models.Prestamo | None:
    """Crea un préstamo si el ítem está disponible."""
    item = db.query(models.ItemBiblioteca).filter(
        models.ItemBiblioteca.id == item_id).first()
    socio = db.query(models.Socio).filter(models.Socio.id == socio_id).first()

    if not item or not socio:
        print("Error: El socio o el ítem no existe.")
        return None

    # Verificación clave: ¿Está el ítem disponible?
    if item.estado != 'disponible':
        print(
            f"Error: El ítem '{item.titulo}' no está disponible para préstamo.")
        return None

    # Si está disponible, cambiamos su estado y creamos el préstamo
    item.estado = 'prestado'
    nuevo_prestamo = models.Prestamo(socio_id=socio_id, item_id=item_id)

    db.add(nuevo_prestamo)
    db.commit()
    print(
        f"Préstamo creado: '{item.titulo}' ha sido prestado a {socio.nombre}.")
    return nuevo_prestamo


def finalizar_prestamo(db: Session, prestamo_id: int) -> models.Prestamo | None:
    """Finaliza un préstamo existente y marca el ítem como disponible."""
    prestamo = db.query(models.Prestamo).filter(
        models.Prestamo.id == prestamo_id).first()

    if not prestamo:
        print(f"Error: No se encontró un préstamo con id {prestamo_id}.")
        return None

    if prestamo.fecha_devolucion is not None:
        print("Error: Este préstamo ya ha sido finalizado.")
        return None

    # Cambiamos la fecha de devolución y el estado del ítem
    prestamo.fecha_devolucion = datetime.date.today()
    prestamo.item.estado = 'disponible'
    db.commit()
    print(f"Devolución registrada: '{prestamo.item.titulo}' ha sido devuelto.")
    return prestamo


def mostrar_prestamos_activos(db: Session):
    """Muestra todos los préstamos que aún no han sido devueltos."""
    print("\n--- Mostrando préstamos activos ---")
    prestamos_activos = db.query(models.Prestamo).filter(
        models.Prestamo.fecha_devolucion == None).all()

    if not prestamos_activos:
        print("No hay préstamos activos en este momento.")
    else:
        for p in prestamos_activos:
            print(
                f"- {p.item.titulo} (prestado a {p.socio.nombre} el {p.fecha_prestamo})")
