# main.py

from biblioteca.database import SessionLocal, init_db
from biblioteca import crud


def main():
    """
    Función principal de la aplicación.
    """
    print("Iniciando aplicación de biblioteca...")

    # 1. Inicializa la base de datos
    init_db()

    # 2. Crea una sesión de base de datos
    db = SessionLocal()

    try:
        # 3. Carga los datos iniciales si es necesario
        crud.cargar_datos_iniciales(db)

        # --- NUEVO: Simulación del flujo de préstamo ---
        print("\n==============================================")
        print("     INICIO DE SIMULACIÓN DE PRÉSTAMOS")
        print("==============================================")

        # Mostramos los préstamos activos (al principio no debería haber ninguno)
        crud.mostrar_prestamos_activos(db)

        # SIMULACIÓN 1: Juan (socio id=1) pide prestado "La Comunidad del Anillo" (item id=1)
        print("\n--> Juan intenta pedir un libro...")
        prestamo_juan = crud.crear_prestamo(db, socio_id=1, item_id=1)

        # SIMULACIÓN 2: Maria (socio id=2) intenta pedir el MISMO libro
        print("\n--> María intenta pedir el mismo libro, que ya está prestado...")
        crud.crear_prestamo(db, socio_id=2, item_id=1)  # Esto debería fallar

        # Mostramos los préstamos activos de nuevo (ahora debería aparecer el de Juan)
        crud.mostrar_prestamos_activos(db)

        # SIMULACIÓN 3: Juan devuelve el libro
        print("\n--> Juan devuelve el libro...")
        if prestamo_juan:
            crud.finalizar_prestamo(db, prestamo_id=prestamo_juan.id)

        # Mostramos los préstamos activos al final (debería estar vacío de nuevo)
        crud.mostrar_prestamos_activos(db)

        print("\n==============================================")
        print("      FIN DE SIMULACIÓN DE PRÉSTAMOS")
        print("==============================================")

    finally:
        # 5. Cierra la sesión
        db.close()
        print("\nAplicación finalizada. Conexión a la base de datos cerrada.")


if __name__ == "__main__":
    main()
