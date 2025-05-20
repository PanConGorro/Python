from colorama import Fore, Back, Style, init    #Importo la biblioteca de colorama
import funciones                                #Importo las funciones

init(autoreset=True)                            #Le indico que se uto resetee

estilo_menu = Back.BLACK + Fore.BLUE

funciones.crear_inventario()                    #Creo el inventario si no existe

def menu():
    funciones.limpiar_pantalla()
    menu = True
    while menu:
        print(estilo_menu + "=============================",
              estilo_menu + Style.BRIGHT + "\n|        INVENTARIO         |",
              estilo_menu + "\n=============================",
              estilo_menu + "\n| 1. Mostrar Inventario     |",
              estilo_menu + "\n| 2. Buscar Producto        |",
              estilo_menu + "\n| 3. Agregar Producto       |",
              estilo_menu + "\n| 4. Modificar Producto     |",
              estilo_menu + "\n| 5. Quitar Producto        |",
              estilo_menu + "\n| 6. Revisar Stock          |",
              estilo_menu+"\n| "+ Fore.RED + "0. Apagar                 "+estilo_menu +"|",
              estilo_menu + "\n=============================",
              end=Fore.CYAN +"\nSelecione una opcion: ")
        
        op = funciones.verificar_rango(0, 6)
        
        funciones.limpiar_pantalla()            #Limpio la pantalla

        opciones = {
            1: funciones.mostrar_inventario,    #Muestro el inventario
            2: funciones.buscar_producto,       #Busco un producto
            3: funciones.agregar_producto,      #Agrego un producto
            4: funciones.modificar_producto,    #Modifico un producto
            5: funciones.eliminar_producto,     #Elimino un producto
            6: funciones.revisar_stock,         #Reviso el stock
        }

        if op in opciones:
            resultado = opciones[op]()          #Ejecuto las opciones y guardo el booleano
            if resultado is False:
                menu = False
            elif resultado is not True:           #Pregunto al usuario si quiere continuar en el programa luego de que se terminen de ejecutar las  
                funciones.tiempo_fuera()        #funciones. En el caso de que el return sea False esto no se pregunta (lo utilizo para el minimenu)
        elif op == 0:
            menu = False                    #Salgo del programa
            
menu()                                          #Ejecuto el programa