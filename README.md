# Inventario
Proyecto realizado en el marco del curso Introducción a Python – Talento Tech 2025.
Consiste en un pequeño sistema de inventario por consola, utilizando Python y SQLite.

🚀 Funcionalidades

Agregar productos

Ver productos

Actualizar productos

Eliminar productos

Buscar productos (por ID, nombre o categoría)

Control de stock

El sistema incluye validaciones, manejo de errores, colores en la interfaz (Colorama) y uso de módulos separados para mantener el código ordenado.

🧱 Tecnologías usadas

Python 3

SQLite (.db)

Colorama

Modularización en Python

Docstrings y buenas prácticas básicas

📂 Estructura del proyecto
main.py               # Punto de entrada del programa
navigation.py         # Manejo del menú y creación de la tabla
actions.py            # Lógica del inventario (CRUD completo)
connections.py        # Conexión y funciones auxiliares de SQLite
inventary.db          # Base de datos

▶️ Cómo ejecutar

Instalar dependencias (solo colorama):

pip install colorama


Ejecutar el programa:

python main.py


La base de datos se crea automáticamente si no existe.

📌 Objetivo del proyecto

Aplicar los conceptos vistos en el curso:

Entrada y salida por consola

Validación de datos

Manejo de excepciones

Funciones y módulos

Uso básico de bases de datos

Buenas prácticas iniciales (docstrings, separación de responsabilidades)
