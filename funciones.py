from colorama import Fore, Back, Style, init
import sqlite3
import os

init(autoreset=True)

####################################################################################################
#Sirve para limpiar la consola, tanto en windows como en otros SO
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')
####################################################################################################

####################################################################################################
#Crea el archivo del inventario si no existe
def crear_inventario():
    conexion = sqlite3.connect("./inventario.db")
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Inventario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    stock INTEGER NOT NULL,
                    precio REAL NOT NULL,
                    categoria TEXT NOT NULL)''')
    conexion.commit()
    conexion.close()
####################################################################################################


####################################################################################################
#Sirve para verificar que se ingrese un dato
def verificar_vacio(valor):
    while len(valor) == 0:
        print(Fore.RED + "EL CAMPO NO PUEDE ESTAR VACIO")
        valor = input(Fore.CYAN + "Ingresar nuevamente: ")
    return valor
####################################################################################################

####################################################################################################
#Sirve para verificar que un número ingresado se encuentre dentro de un rango determinado
def verificar_rango(n1, n2):
    while True:
        try:
            ni = int(input(Fore.CYAN+""))
            if ni >= n1 or ni <= n2:
                return ni
            print(Fore.CYAN +f"Ingrése un número dentro del rango ({n1}-{n2})")
        except ValueError:
            print(Fore.CYAN +"Ingresar un valor válido")
            ni = n1 - 1
####################################################################################################

####################################################################################################
#Sirve para que la consola se pause y pregunta al usuario si se desea continuar en el programa
def tiempo_fuera():
    op = -1
    while op < 0 or op > 1:
        print(Fore.CYAN + "==========================",
               Fore.LIGHTGREEN_EX + "\n1. Volver"  + Fore.RED + "   0. Apagar",
                Fore.CYAN + "\n==========================",)
        op = verificar_rango(0, 1)
        if op == 0:
            exit()
        limpiar_pantalla()
####################################################################################################

####################################################################################################
#Sirve para pedir un numero entero positivo
def pedir_numero_entero(min = 0):           #Se espera que se ingrese el número mínimo que se puede elegir, si no, será 0
    while True:
        try:
            numero = int(input(Fore.CYAN+""))
            if numero < min:
                print(Fore.RED +"Ingresar un valor válido")
            if numero >= min:
                return numero
        except ValueError as e:
            print(Fore.RED +"Tenes que ingresar un valor válido")

#Sirve para pedir un numero flotante 
def pedir_numero_flotante(min = 0):
    while True:
        try:
            numero = float(input(Fore.CYAN+""))
            if numero < min:
                print(Fore.RED +"Ingresar un valor válido")
            if numero >= min:
                return numero
        except ValueError as e:
            print(Fore.RED +"Tenes que ingresar un valor válido")
####################################################################################################

####################################################################################################
#Sirve para mostrar el Inventario
def mostrar_inventario(inventario = []):
    print(Fore.BLUE + "==============================================================================")
    if len(inventario) == 0:
        conexion = sqlite3.connect("./inventario.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Inventario")
        resultados = cursor.fetchall()
        print(Fore.BLUE + Style.BRIGHT + f"{"ID":<5}{"nombre":<15}{"descripcion":<20}{"cantidad":<10}{"precio":<10}{"categoria":<10}")
        if not resultados:
            print(Fore.BLUE + "==============================================================================")
            print(Fore.RED + "=============================",
                Fore.RED + Style.BRIGHT + "\n     INVENTARIO VACIO",
                Fore.RED + "\n=============================")
            conexion.close()
            return
        for registro in resultados:      
            print(Fore.CYAN +f"{registro[0]:<5}{registro[1]:<15}{registro[2]:<20}{registro[3]:<10}${registro[4]:<9}{registro[5]:<10}")
        print(Fore.BLUE + "==============================================================================")
        conexion.close()
    else:
        print(Fore.BLUE + Style.BRIGHT + f"{"ID":<5}{"nombre":<15}{"descripcion":<20}{"cantidad":<10}{"precio":<10}{"categoria":<10}")
        for registro in inventario:
            print(Fore.CYAN +f"{registro[0]:<5}{registro[1]:<15}{registro[2]:<20}{registro[3]:<10}${registro[4]:<9}{registro[5]:<10}")
        print(Fore.BLUE +"==============================================================================")
####################################################################################################

####################################################################################################
#Sirve para buscar un producto del inventario por ID, por NOMBRE o por CATEGORIA
def buscar_producto():
    minimenu = True
    while minimenu == True:
        limpiar_pantalla()
        print(Fore.BLUE +"===========================",
            Fore.BLUE +"\n| 1. Buscar por categoria |",
            Fore.BLUE +"\n| 2. Buscar por nombre    |",
            Fore.BLUE +"\n| 3. Buscar por ID        |",
            Fore.BLUE +"\n|"+Fore.MAGENTA +" 0. Volver               "+Fore.BLUE +"|",
            Fore.BLUE +"\n===========================")
        print(end=Fore.CYAN +"Selecione una opcion: "); op = verificar_rango(0, 2)
        limpiar_pantalla()

        #Sale del mini menu
        if op == 0:
            return True     #Devuelve un "True" para que en el nemú no repita la función "tiempo_fuera()"

        #Filtra por categoria
        if op == 1:
            busqueda('categoria','Categoria')

        #Filtra por nombre
        if op == 2:
            busqueda('nombre','Nombre')
        
        #Filtra por ID
        if op == 3:
            busqueda('id','ID')
        
#Sirve para realizar las busquedas
def busqueda(cni, m): #[(Categoria, Nombre o ID), (mensaje)]
    limpiar_pantalla()
    conexion = sqlite3.connect("./inventario.db")
    cursor = conexion.cursor()
    print(Fore.BLUE +"============================================")
    valor = input(Fore.CYAN +f"{m} del producto a buscar: ").capitalize()
    valor = verificar_vacio(valor)
    mensaje = f"SELECT * FROM Inventario WHERE {cni} = ?"
    cursor.execute(mensaje, (valor,))
    resultado = cursor.fetchall()
    print(Fore.BLUE +"============================================")
    if resultado:
        mostrar_inventario(resultado)
    else:
        print(Fore.RED + Style.BRIGHT +"      NINGUNA COINCIDENCIA ENCONTRADA",
              Fore.BLUE +"\n============================================")
    conexion.close()
    tiempo_fuera()
####################################################################################################
    
####################################################################################################
#Sirve para agregar un producto al inventario (o modificarlo dependiendo el caso)
def agregar_producto(ide = 0):
    limpiar_pantalla()
    conexion = sqlite3.connect("./inventario.db")
    cursor = conexion.cursor()
    if ide != 0:            #Este if lo utilizo para modificar producto
        cursor.execute('''SELECT * FROM Inventario WHERE id = ?''', (ide,))
        resultado = cursor.fetchone()
        mostrar_inventario([resultado])     #Me muestra los datos del producto antes de modificarlo
        print(Fore.BLUE +"=======================================")
        print(Fore.BLUE + Style.BRIGHT+"             DATOS NUEVOS",
              Fore.BLUE +"\n=======================================")
    else:                                   #Si no se va a modificar un producto, lo agrega
        print(Fore.BLUE +"=======================================")
        print(Fore.BLUE + Style.BRIGHT+"                DATOS",
              Fore.BLUE +"\n=======================================")
    nombre = input(Fore.CYAN +"Nombre: ").capitalize()
    nombre = verificar_vacio(nombre)
    descripcion = input(Fore.CYAN +"Descripcion: ").capitalize()
    descripcion = verificar_vacio(descripcion)
    print(end=Fore.CYAN +"Cantidad: "); stock = pedir_numero_entero()
    print(end=Fore.CYAN +"Precio: $"); precio = pedir_numero_flotante()    #Permito que se ingrese un número negativo para darle más libertad al usuario respecto a los valores que quiera ingresar
    categoria = input(Fore.CYAN +"Categoria: ").capitalize()
    categoria = verificar_vacio(categoria)
    if ide != 0:        #Lo uso para modificar un producto
        #Antes de modificar confirmo los cambios
        if confirmar_modificacion(ide, nombre, descripcion, stock, precio, categoria):
            cursor.execute('''UPDATE Inventario SET nombre = ?, descripcion = ?, stock = ?, precio = ?, categoria = ? WHERE id = ?''',
                       (nombre, descripcion, stock, precio, categoria, ide))
            conexion.commit()

    else:               #Lo uso para agregar un producto
        #Confirmo si se quiere agregar el producto
        if confirmar_producto(nombre, descripcion, stock, precio, categoria):
            cursor.execute('''INSERT INTO Inventario(nombre, descripcion, stock, precio, categoria) VALUES (?, ?, ?, ?, ?)''',
                    (nombre, descripcion, stock, precio, categoria))
            conexion.commit()
    conexion.close()

#Sirve para que el usuario pueda confirmar si quiere agregar el nuevo producto
def confirmar_producto(nombre, descripcion, stock, precio, categoria):
    limpiar_pantalla()
    producto_nuevo = ["-    ", nombre, descripcion, stock, precio, categoria]
    print(Fore.BLUE + Style.BRIGHT +"DATOS DEL PRODUCTO:")
    mostrar_inventario([producto_nuevo])
    while True:
        print(Fore.BLUE +"===================================",
            Fore.BLUE + Style.BRIGHT +"\n|    CONFIRMAR NUEVO PRODUCTO     |",
            Fore.BLUE +"\n===================================",
            Fore.BLUE +"\n|"+Fore.GREEN +" 1.Confirmar producto            "+Fore.BLUE +"|",
            Fore.BLUE +"\n|"+Fore.RED +" 0.Cancelar ingreso              "+Fore.BLUE +"|",
            Fore.BLUE +"\n===================================")
        print(end=Fore.CYAN +"Selecione una opcion: "); op = verificar_rango(0, 1)
        if op == 1:
            limpiar_pantalla()
            print(Fore.GREEN +"=======================================",
                Fore.GREEN + Style.BRIGHT +"\n|   PRODUCTO AGREGADO CORRECTAMENTE   |",
                Fore.GREEN +"\n=======================================")
            return True
        if op == 0:
            limpiar_pantalla()
            print(Fore.RED +"=======================================",
                Fore.RED + Style.BRIGHT +"\n|        PRODUCTO NO AGREGADO         |",
                Fore.RED +"\n=======================================")
            return False
####################################################################################################

####################################################################################################
#Sirve para modificar un producto del inventario en base a su ID
def modificar_producto():
    limpiar_pantalla()
    conexion = sqlite3.connect("./inventario.db")
    cursor = conexion.cursor()
    cursor.execute('''SELECT * FROM Inventario''')
    inv = cursor.fetchall()
    mostrar_inventario()                #Muestro primero el inventario para que el usuario pueda visualizar lo que va a modificar
    if not inv:
        print(Fore.RED + "=======================================",
              Fore.RED + Style.BRIGHT +"\n|         INVENTARIO VACIO            |",
              Fore.RED + "\n=======================================")
        conexion.close()
        return
    
    print(end=Fore.CYAN +"Ingresar ID del producto que se desea modificar (0 para volver): ")
    verifico = True
    ide = pedir_numero_entero(0)
    if(ide == 0):
            verifico = False
            limpiar_pantalla()
            return True
    while verifico:
        
        cursor.execute('''SELECT * FROM Inventario WHERE id = ?''', (ide,))
        producto = cursor.fetchone()
        
        if producto:
            agregar_producto(ide)
            conexion.close()
            verifico = False
        else:
            print(Fore.RED +"=========================================",
              Fore.RED + Style.BRIGHT +"\n| ID NO ENCONTRADO, INTENTAR NUEVAMENTE |",
              Fore.RED +"\n=========================================")
            ide = pedir_numero_entero(0)

def confirmar_modificacion(ide, nombre, descripcion, stock, precio, categoria):
    limpiar_pantalla()
    producto_nuevo = [ide, nombre, descripcion, stock, precio, categoria]
    print("PRODUCTO ACTUALIZADO:")
    mostrar_inventario([producto_nuevo])
    while True:
        print(Fore.BLUE +"===================================",
            Fore.BLUE + Style.BRIGHT + "\n|   DESEA CONFIRMAR LOS CAMBIOS?  |",
            Fore.BLUE +"\n===================================",
            Fore.BLUE +"\n|"+Fore.GREEN +" 1. Guardar cambios              "+Fore.BLUE +"|",
            Fore.BLUE +"\n| "+Fore.RED +"0. Cancelar cambios             "+Fore.BLUE +"|",
            Fore.BLUE +"\n===================================")
        print(end=Fore.CYAN +"Selecione una opcion: "); op = verificar_rango(0, 1)
        if op == 1:
            limpiar_pantalla()
            print(Fore.GREEN +"=======================================",
                Fore.GREEN +"\n| PRODUCTO ACTUALIZADO CORRECTAMENTE  |",
                Fore.GREEN +"\n=======================================")
            return True
        if op == 0:
            limpiar_pantalla()
            print(Fore.RED +"=======================================",
                Fore.RED + Style.BRIGHT +"\n|      PRODUCTO NO ACTUALIZADO        |",
                Fore.RED +"\n=======================================")
            return False
####################################################################################################

####################################################################################################
#Sirve para eliminar un producto en base al ID
def eliminar_producto():
    limpiar_pantalla()
    conexion = sqlite3.connect("./inventario.db")
    cursor = conexion.cursor()
    cursor.execute('''SELECT * FROM Inventario''')
    inv = cursor.fetchall()
    mostrar_inventario()
    if not inv:
        print(Fore.RED +"=======================================",
              Fore.RED + Style.BRIGHT +"\n|         INVENTARIO VACIO            |",
              Fore.RED +"\n=======================================")
        conexion.close()
        return
    
    print(end=Fore.CYAN +"Ingresar ID del producto que se desea eliminar (0 para volver): ")
    verifico = True
    ide = pedir_numero_entero(0)
    if ide == 0:
        verifico = False
        limpiar_pantalla()
        return True
    while verifico:
        cursor.execute('''SELECT * FROM Inventario WHERE id = ?''', (ide,))
        producto = cursor.fetchone()

        if producto:
            verifico = True
            while verifico:
                limpiar_pantalla()
                print(Fore.BLUE+"========================================================",
                    Fore.BLUE+f"\n|   DESEA ELIMINAR ESTE PRODUCTO DE FORMA "+Fore.LIGHTRED_EX+"PERMANENTE"+Fore.BLUE+"?  |",
                    Fore.BLUE+"\n========================================================")
                mostrar_inventario([producto])
                print(Fore.CYAN+"=================================",
                    Fore.CYAN+"\n"+Fore.GREEN+"| 1. Confirmar"+Fore.RED+"    0. Cancelar   "+Fore.CYAN+"|",
                    Fore.CYAN+"\n=================================",
                    end=Fore.CYAN+"\nSelecione una opcion: ")
                op = verificar_rango(0, 1)
                if op == 1:
                    limpiar_pantalla()
                    cursor.execute('''DELETE FROM Inventario WHERE id = ?''',(ide,))
                    conexion.commit()
                    conexion.close()
                    print(Fore.GREEN+"=======================================",
                        Fore.GREEN+"\n|  PRODUCTO ELIMINADO CORRECTAMENTE   |",
                        Fore.GREEN+"\n=======================================")
                    verifico = False
                if op == 0:
                    limpiar_pantalla()
                    print(Fore.RED +"=======================================",
                        Fore.RED + Style.BRIGHT + "\n|       PRODUCTO NO ELIMINADO         |",
                        Fore.RED +"\n=======================================")
                    verifico = False

        else:
            print(Fore.RED +"=========================================",
              Fore.RED +  Style.BRIGHT + "\n| ID NO ENCONTRADO, INTENTAR NUEVAMENTE |",
              Fore.RED +"\n=========================================")
####################################################################################################

####################################################################################################
#Sirve para revisar el stock en base a una cantidad maxima
def revisar_stock():
    limpiar_pantalla()
    conexion = sqlite3.connect("./inventario.db")
    cursor = conexion.cursor()
    print(Fore.BLUE+"==============================================")
    print(end=Fore.CYAN+"Mostrar productos con un stock menor a: "); stock = pedir_numero_entero()
    cursor.execute('''SELECT * FROM Inventario WHERE stock <= ?''', (stock,))
    print(Fore.BLUE+"==============================================")
    resultados = cursor.fetchall()
    if resultados:
        mostrar_inventario(resultados) 
    else:
        limpiar_pantalla()
        print(Fore.RED +"=================================================",
              Fore.RED + Style.BRIGHT+f"\n|   NO HAY PRODUCTOS CON UN STOCK MENOR A {stock}\t|",
              Fore.RED +"\n=================================================") 
    conexion.close()
####################################################################################################