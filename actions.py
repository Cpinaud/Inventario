import connections
from colorama import Fore, Style, init

init(autoreset=True)

def add():
    '''
    Agrega un elemento a la tabla products solicitando y validando los datos de entrada.

    Muestra mensajes si algo falla y solicita reingresar datos.

    :return: Devuelve un mensaje de finalización exitosa
    '''
    connection,cursor = connections.connect()
    while True:
        try:
            ##Entrada de datos por parte del usuario
            name = input(Fore.CYAN +"ingrese el nombre del producto:\n"+ Style.RESET_ALL)
            description = input(Fore.CYAN +"ingrese la descripción del producto:\n"+ Style.RESET_ALL)
            category = input(Fore.CYAN +"ingrese la categoría del producto:\n"+ Style.RESET_ALL)            
            stock = int(input(Fore.CYAN +"ingrese el stock actual del producto:\n"+ Style.RESET_ALL))
            price = float(input(Fore.CYAN +"ingrese el precio del producto:\n"+ Style.RESET_ALL))
            ##validaciones
            if not name:
                print(Fore.RED + Style.BRIGHT+"El nombre no puede estar vacío")
            elif not int(price)>0:
                print(Fore.RED + Style.BRIGHT+"El precio del producto debe ser mayor a cero")
            else:
                #seteo de campos por default y normalización + insert
                if not description:
                    description = "Producto sin descripción"
                if not category:
                    category = "VARIOS"
                name = name.strip().capitalize()
                description = description.strip().capitalize()
                category = category.strip().upper()
                query = '''
                    INSERT INTO products (name, description, category, stock, price)
                    VALUES (?, ?, ?, ?, ?)
                    '''
                params = (name, description, category, stock, price)
                connections.execute(cursor, query, connection,params)
                break
        except ValueError:
            print(Fore.RED + Style.BRIGHT+"debe ingresar un valor numérico")
    connections.close(connection)
    return Fore.GREEN + Style.BRIGHT+"Producto agregado."

def search_products(condition="",value=""):
    """
    Busca productos en la tabla 'products' según un campo y un valor.

    Realiza una consulta filtrando por la condición especificada y retorna
    los elementos que coincidan.

    :param condition: Campo por el cual se filtrará la búsqueda.
    :param value: Valor que debe coincidir en el campo indicado.
    :return: Lista de productos que cumplen la condición.
    """
    connection,cursor = connections.connect()
    where = ""
    params = []
    ##Armo el where dependiendo del filtro indicado por parámetros
    if condition:
        match condition:
            case "stock":
                where = f"where {condition} <= ?"
            case "id"|"name"|"category":
                where = f"where {condition} = ?"

        params = (value,)
    query = f"SELECT * FROM products {where}"
    connections.execute(cursor,query, connection,params)
    products = connections.select(cursor)
    connections.close(connection)
    if not len(products)==0:
        return products
    
def show(products):
    '''
    Arma la lista de productos generada en search_products de una forma mas amigable para el usuario.
    
    :param products: Lista de productos generada en funcion search_products
    :return: Devuelve un texto en forma de lista con cada producto o un mensaje de inexistencia en caso de corresponder.
    '''
    if not products:
        return Fore.WHITE + Style.NORMAL+"No existen productos."
    salida = ""
    for id, name,description, stock,price,category in products:
        salida += Fore.WHITE + Style.NORMAL+f"\n{id}. {name} ( {description} ) - {category}. ${price} - {stock} existencias."
    return salida

def stock():
    '''
    Busca elementos de la tabla 'products' que no cumplan con el valor máximo de stock indicado
    
    Solicita un valor numérico y llama a search_products para buscar qué elementos en la tabla 'products' 
    tienen un stock menor o igual al número ingresado.

    :return: Devuelve una lista de productos a reponer.
    '''
    if not search_products():
        return Fore.WHITE + Style.NORMAL+"No existen productos."
    else:
        while True:
            try:
                limit = int(input(Fore.CYAN +"Ingrese la cantidad mínima a controlar: "+ Style.RESET_ALL))
                if limit>0:
                    print(Fore.WHITE + Style.NORMAL+"Productos a reponer:")
                    return show(search_products("stock",limit))
                else:
                    print(Fore.RED + Style.BRIGHT+"debe ingresar un valor mayor a 0")
            except ValueError:
                print(Fore.RED + Style.BRIGHT+"debe ingresar un valor numérico")

def delete():
    '''
    Elimina un elemento de la tabla products 

    Solicita el ingreso de un ID y hace una búsqueda a través de search_products para verificar la existencia del elemento
    en la tabla 'products'. De no existir, se informa. En caso de que haya existencia, se solicita al usuario confirmación 
    para realizar la acción de eliminado

    :return: Devuelve si el elemento fue eliminado o la operación fue cancelada, según corresponda.
    '''
    if not search_products():
        retorno= Fore.WHITE + Style.NORMAL+"No existen productos."
    else:
        while True:
            try:
                id = int(input(Fore.CYAN +"Ingrese el id del producto a eliminar o 0 para volver al menú: "+ Style.RESET_ALL))
                if id==0:
                    retorno=""
                    break
                resultado = search_products("id",id)
                if not resultado or not isinstance(resultado, (list, tuple, set)):
                    print(Fore.MAGENTA+"ID inexistente.")
                else:
                    while True:
                        ##Se solicita confirmación para eliminar
                        confirma = input (Fore.YELLOW+f"Desea eliminar el siguiente producto?: {show(resultado)} \n "+Fore.YELLOW+"SI/NO \n")
                        if confirma.upper()=='NO':
                            retorno = Fore.GREEN + Style.BRIGHT+"Operacion cancelada."
                            break
                        elif confirma.upper()=='SI':
                            connection,cursor = connections.connect()
                            query = "DELETE from products Where id=?"
                            params = (id,)
                            connections.execute(cursor,query, connection,params)
                            connections.close(connection)
                            retorno = Fore.GREEN + Style.BRIGHT+"Producto eliminado."
                            break
                        else:
                            print(Fore.RED + Style.BRIGHT+"opción inválida.")
                    break
            except ValueError:
                print(Fore.RED + Style.BRIGHT+"Debe ingresar un ID válido (numérico)")
    return retorno            

def search():
    '''
    Busca productos según un filtro indicado

    Realiza una búsqueda mediante la funcion search_products a través de los filtros indicados en un submenú,
    validando los datos de entrada

    :return: Lista de elementos encontrados según búsqueda.
    '''
    if not search_products():
        return Fore.WHITE + Style.NORMAL+"No existen productos."
    else:
        search=0
        while True:
            try:
                print()
                print(Fore.BLUE + Style.BRIGHT + "¿Cómo desea filtrar la búsqueda?")
                print(Fore.BLUE + "1. ID del producto")
                print(Fore.BLUE + "2. Nombre del producto")
                print(Fore.BLUE + "3. Categoría del producto")
                print()
                search=int(input())
                match search:
                    case 1:
                        try:
                            id= int(input(Fore.CYAN +"Ingrese el ID del producto a buscar:\n"+ Style.RESET_ALL))
                            return show(search_products("id",id))
                        except ValueError:
                            print(Fore.RED + Style.BRIGHT+"El ID debe ser un valor numérico")
                    case 2:
                        name = input(Fore.CYAN +"Ingrese el nombre del producto a buscar:\n"+ Style.RESET_ALL)
                        if name:
                            name = name.strip().lower().capitalize()
                            return show(search_products("name",name))
                        else:
                            return Fore.MAGENTA+"No existen productos sin nombre."
                    case 3:
                        category = input(Fore.CYAN +"Ingrese la categoría a buscar:\n"+ Style.RESET_ALL)
                        if category:
                            category = category.upper()
                        else:
                            category = "varios"
                        return show(search_products("category",category))
                    case _:
                        print(Fore.RED + Style.BRIGHT+"opción inválida")
            except ValueError:
                print(Fore.RED + Style.BRIGHT+"Debe ingresar una opción numérica válida")

def mapping_product(resultado):
    ##se mapea un elemento a dict para usarlo mas cómodamente en update()
    ##siempre será 1 elemento ya que se busca por ID y es único
    for id, name,description, stock,price,category in resultado:
        product = {
            "id": id,
            "name": name,
            "description": description,
            "category": category,
            "stock": stock,
            "price": price
        }
    return product

def update():
    '''
    Edita datos de un producto a partir de su ID

    Realiza una búsqueda mediante la funcion search_products a través del ID ingresado.
    Muestra un pequeño menú para que el usuario seleccione el dato a modificar
    Valida entrada y edita el dato solicitado.

    :return: Mensaje de confirmación y producto actualizado.
    '''
    if not search_products():
        retorno= Fore.WHITE + Style.NORMAL+"No existen productos."
    else:
        while True:
            try:
                connection,cursor = connections.connect()
                id = int(input(Fore.CYAN +"Ingrese el id del producto a editar o 0 para volver al menú: "+ Style.RESET_ALL))
                if id==0:
                    retorno=""
                    break
                resultado = search_products("id",id)
                if not resultado or not isinstance(resultado, (list, tuple, set)):
                    print(Fore.MAGENTA+"ID inexistente.")
                else:
                    product = mapping_product(resultado)
                    print(show(resultado))

                    while True:
                        try:
                            print()
                            print(Fore.BLUE + Style.BRIGHT + "Qué dato desea editar?")
                            print(Fore.BLUE + "1. Nombre")
                            print(Fore.BLUE + "2. Descripción")
                            print(Fore.BLUE + "3. Categoría")
                            print(Fore.BLUE + "4. Precio")
                            print(Fore.BLUE + "5. Stock")
                            print()
                            field = int(input ())
                            valid=True
                            match field:
                                case 1:
                                    print(Fore.WHITE + Style.NORMAL+f"Nombre actual: {product["name"]}")
                                    name = input(Fore.CYAN +"Ingrese el nuevo nombre: \n"+ Style.RESET_ALL)
                                    if not name:
                                        name = product["name"]
                                    field="name"
                                    value=name.strip().capitalize()                                
                                case 2:
                                    print(Fore.WHITE + Style.NORMAL+f"Descripcion actual: {product["description"]}")
                                    description = input(Fore.CYAN +"Ingrese la nueva descripcion: \n"+ Style.RESET_ALL)
                                    if not description:
                                        description = product["description"]
                                    field="description"
                                    value=description.strip().capitalize()
                                case 3:
                                    print(Fore.WHITE + Style.NORMAL+f"Categoría actual: {product["category"]}")
                                    category = input(Fore.CYAN +"Ingrese la nueva categoría: \n"+ Style.RESET_ALL)
                                    if not category:
                                        category = product["category"]
                                    field="category"
                                    value=category.upper()
                                case 4:
                                    print(Fore.WHITE + Style.NORMAL+f"Precio actual: ${product["price"]}")
                                    try:
                                        price = int(input(Fore.CYAN +"Ingrese el nuevo precio: \n"+ Style.RESET_ALL))
                                        if price>0:
                                            field="price"
                                            value=price 
                                        else:
                                            valid=False
                                            print(Fore.RED + Style.BRIGHT+"El precio debe ser mayor a 0")
                                    except ValueError:
                                        valid=False
                                        print(Fore.RED + Style.BRIGHT+"El precio debe ser mayor a 0")
                                case 5:
                                    print(Fore.WHITE + Style.NORMAL+f"Stock actual: {product["stock"]}")
                                    try:
                                        stock = int(input(Fore.CYAN +"Ingrese el nuevo stock: \n"+ Style.RESET_ALL))
                                        if stock>=0:
                                            field="stock"
                                            value=stock 
                                        else:
                                            valid=False
                                            print(Fore.RED + Style.BRIGHT+"El stock debe ser mayor o igual a 0")
                                    except ValueError:
                                        valid=False
                                        print(Fore.RED + Style.BRIGHT+"El stock debe ser mayor o igual a 0")
                                case _:
                                    valid=False
                                    print(Fore.RED + Style.BRIGHT+"opción inválida.")
                            if valid:
                                query = f"UPDATE products Set {field} = ? Where id=?"
                                params = (value,id)
                                connections.execute(cursor,query, connection,params)
                                resultado = search_products("id",id)
                                connections.close(connection)
                                retorno = Fore.GREEN + Style.BRIGHT+f"Producto modificado: \n {show(resultado)}"
                                break
                        except ValueError:
                            print(Fore.RED + Style.BRIGHT+"Debe ingresar una opción numérica.\n")
                    break
            except ValueError:
                print(Fore.RED + Style.BRIGHT+"Debe ingresar un ID válido (numérico)")
    return retorno