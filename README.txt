===================================================================
                        GESTOR DE INVENTARIO
===================================================================

Descripción General:
Este programa permite gestionar un inventario utilizando una base de datos SQLite. 
Ofrece funcionalidades como mostrar, buscar, agregar, modificar, y eliminar productos, 
además de verificar el stock disponible.

-------------------------------------------------------------------

Requisitos Previos:
- Python 3.8 o superior
- Biblioteca "colorama" (puede instalarse con 'pip install colorama')

-------------------------------------------------------------------

Instrucciones de Instalación:
1. Asegúrate de tener Python 3 instalado en tu sistema.
2. Descarga e instala la biblioteca "colorama" ejecutando:
   'pip install colorama'
3. Descarga los archivos del programa:
   - menu.py
   - funciones.py
4. Guarda los archivos en el mismo directorio.

-------------------------------------------------------------------

Modo de uso:
1. Ejecuta el archivo 'menu.py' para iniciar el programa:
   'python menu.py'
2. Aparecerá un menú principal en la consola con las siguientes opciones:
   - Mostrar Inventario: Visualiza todos los productos registrados.
   - Buscar Producto: Encuentra productos por ID, nombre o categoría.
   - Agregar Producto: Añade un nuevo producto al inventario.
   - Modificar Producto: Cambia la información de un producto existente.
   - Quitar Producto: Elimina un producto del inventario.
   - Revisar Stock: Consulta los productos con cantidades limitadas.
   - Apagar: Cierra el programa.

3. Selecciona una opción escribiendo el número correspondiente.

-------------------------------------------------------------------

Estructura del Código:
- 'menu.py': Contiene el menú principal y la lógica para interactuar con el usuario.
- 'funciones.py': Contiene todas las funciones necesarias para realizar las operaciones
  del programa, como conexión a la base de datos, validación de datos y manejo de errores.

-------------------------------------------------------------------

Creado por Tomás Flores.
tomasfloresdiener@gmail.com

-------------------------------------------------------------------