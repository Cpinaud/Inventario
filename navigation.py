import connections
import actions
from colorama import Fore, Style, init

init(autoreset=True)

def start():
    '''Función que inicia el programa 
    creando la tabla products si es necesario'''
    connection,cursor = connections.connect()
    query='''
                 CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    description TEXT, 
    stock INTEGER NOT NULL,
    price FLOAT NOT NULL,
    category TEXT)
                 '''
    connections.execute(cursor,query,connection)
    connections.close(connection)

def mostrar_menu():
    '''Función que agrupa las opciones 
    a mostrar en el menú interactivo'''
    print()
    print(Fore.CYAN + Style.BRIGHT +"********************")
    print(Fore.CYAN + Style.BRIGHT +"***MENÚ PRINCIPAL***")
    print(Fore.CYAN + Style.BRIGHT +"********************")
    print()
    print(Fore.CYAN + Style.BRIGHT + "Ingrese la opción deseada:")
    print(Fore.CYAN + "1. Agregar producto")
    print(Fore.CYAN + "2. Ver productos")
    print(Fore.CYAN + "3. Actualizar producto")
    print(Fore.CYAN + "4. Eliminar producto")
    print(Fore.CYAN + "5. Buscar productos")
    print(Fore.CYAN + "6. Control de stock")
    print(Fore.CYAN + "7. Salir")
    print()
    option = input()
    return option

def menu():
    '''
    Función que maneja las opciones del 
    menú interactivo y devuelve lo solicitado
    '''
    option= mostrar_menu()
    if not option or not option.isdigit:
        option=100
    option=int(option)
    while(option!=7):
        match option:
            case 1:
                resultado= actions.add()
            case 2:
                resultado= actions.show(actions.search_products())
            case 3:
                resultado= actions.update()
            case 4:
                resultado= actions.delete()
            case 5:
                resultado = actions.search()
            case 6:
                resultado= actions.stock()
            case _:
                resultado =Fore.RED + Style.BRIGHT+"\n opcion inválida. \n"
        print(resultado)
        option= mostrar_menu()
        if option.isdigit():
                option=int(option)
    print(Fore.WHITE + Style.NORMAL+"Hasta pronto!")