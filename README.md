# Sistema de Gestión de Biblioteca Virtual

Proyecto desarrollado para la materia **Programación Avanzada**. Es un sistema de software diseñado para administrar de forma eficiente el catálogo, los socios y los préstamos de una biblioteca. Utiliza Python y el ORM SQLAlchemy para interactuar con una base de datos relacional, asegurando la persistencia y la integridad de los datos.

## Características Principales

* **Gestión del Catálogo:** Permite realizar operaciones CRUD (Crear, Leer, Actualizar, Borrar) sobre los ítems de la biblioteca. Soporta diferentes tipos de publicaciones (Libros, Revistas) mediante herencia polimórfica.
* **Administración de Socios:** Gestión completa de los miembros de la biblioteca, incluyendo registro y consulta de datos.
* **Control de Préstamos:** Sistema para registrar préstamos y devoluciones, asociando cada ítem a un socio y controlando su estado (disponible, prestado).
* **Gestión de Entidades Relacionadas:** Administración de autores y géneros para una catalogación más detallada de los libros.
* **Persistencia de Datos:** Toda la información es almacenada y gestionada en una base de datos SQL, garantizando que los datos no se pierdan al cerrar la aplicación.
* **Interfaz de Usuario por Consola:** Interacción con el sistema a través de un menú de opciones claro y sencillo en la terminal.

## Tecnologías Utilizadas

* **Lenguaje:** Python 3
* **Base de Datos:** SQLAlchemy (ORM)
* **Motor de BD:** SQLite (configurado por defecto para portabilidad)

## Esquema de la Base de Datos

El diseño se centra en una estructura relacional normalizada para evitar la redundancia y mantener la consistencia de los datos. Las tablas principales son:

* `items_biblioteca`: Tabla central que almacena los datos comunes a todas las publicaciones.
* `libros` y `revistas`: Subclases que heredan de `items_biblioteca` y contienen campos específicos.
* `autores` y `generos`: Tablas de catálogo para enriquecer la información de los libros.
* `socios`: Almacena los datos de los miembros habilitados para solicitar préstamos.
* `prestamos`: Tabla transaccional que conecta a los `socios` con los `items_biblioteca`, registrando las fechas de préstamo y devolución.

## Instalación

Para ejecutar este proyecto en un entorno local, sigue estos pasos:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
    cd tu-repositorio
    ```

2.  **Crear un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Asegúrate de tener un archivo `requirements.txt` con las librerías necesarias, como `SQLAlchemy`).*

## Uso

Una vez instaladas las dependencias, el programa se ejecuta desde la raíz del proyecto:

```bash
python main.py
