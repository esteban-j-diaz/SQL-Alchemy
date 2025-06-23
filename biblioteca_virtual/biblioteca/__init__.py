# biblioteca/__init__.py (Versión actualizada para el sistema de préstamos)

# Importamos las funciones y clases más importantes de cada módulo
# para que estén disponibles directamente desde el paquete 'biblioteca'.

from .database import SessionLocal, init_db
from .models import Autor, Genero, Libro, Revista, ItemBiblioteca, Socio, Prestamo

# Aquí está el cambio: quitamos la función vieja y añadimos las nuevas de crud.py
from .crud import cargar_datos_iniciales, crear_prestamo, finalizar_prestamo, mostrar_prestamos_activos
