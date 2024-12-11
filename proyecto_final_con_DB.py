import sqlite3

# ---------------------------------------------------------------------------- #
#                          CONEXIóN A LA BASE DE DATOS                         #
# ---------------------------------------------------------------------------- #
def enlace_conexion():
    conexion = sqlite3.connect("inventario.db")
    conexion.row_factory = sqlite3.Row
    cursor =  conexion.cursor()
    return cursor, conexion

# ---------------------------------------------------------------------------- #
#                               CREAR INVENTARIO                               #
# ---------------------------------------------------------------------------- #
def crear_inventario():
    cursor, conexion = enlace_conexion()
    query = """
        CREATE TABLE IF NOT EXISTS Productos(
            id_producto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(25) NOT NULL,
            descripcion VARCHAR(25),
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL,
            categoria VARCHAR(15)
        )
    """
    try:
        cursor.execute(query)
        conexion.commit()
    except sqlite3.Error as e:
        print(f"Error al crear la tabla: {e}")
    finally:
        conexion.close()

# ---------------------------------------------------------------------------- #
#                                VALIDAR PRECIO                                #
# ---------------------------------------------------------------------------- #
def validar_precio():
    #mientras el usuario no ingrese correctamente el valor del producto, se le volverá a solicitar.
    #de esta manera nos aseguramos de que no se ingresen números negativos o cero
    while True:
        monto = float(input("Ingrese el precio del producto: "))
        if monto > 0:
            break
        else:
            print("El precio del producto debe ser mayor que 0, ingrese un valor válido")
    return monto

# ---------------------------------------------------------------------------- #
#                                 VALIDAR STOCK                                #
# ---------------------------------------------------------------------------- #
def validar_stock():
    #mientras el usuario no ingrese correctamente la cantidad correcta del producto, se le volverá a solicitar.
    #de esta manera nos aseguramos de que no se ingresen números negativos
    while True:
        cantidad = int(input("Ingrese la cantidad de existencias del producto: "))
        if cantidad >= 0:
            break
        else:
            print("La cantidad del producto no puede ser inferior a 0, vuelva a intentar")
    return cantidad

# ---------------------------------------------------------------------------- #
#                             MOSTRAR COINCIDENCIAS                            #
# ---------------------------------------------------------------------------- #
def mostrar_coincidencias(resultados):
    #esta función muestra los registros que coincidentes en una tabla formatada con rjust, ljust y center
    #recibe como parametro una lista que se itera con un bucle for mostrando los diferentes datos que contiene
    print("ID".ljust(10) ,"Producto".ljust(25), "Descripción".ljust(25), "Precio".center(10), "Cantidad".rjust(10), "Categoría".rjust(15))
    for registro in resultados:
        print(f"{registro['id_producto']}".ljust(10), f"{registro['nombre']}".ljust(25), f"{registro['descripcion']}".ljust(25), f"${registro['precio']}".center(10), f"{registro['cantidad']}".rjust(10), f"{registro['categoria']}".rjust(15))
    print()

# ---------------------------------------------------------------------------- #
#                                INSERTAR REGISTROS                            #
# ---------------------------------------------------------------------------- #
def insertar():
    cursor, conexion = enlace_conexion()
    query = """
        INSERT INTO Productos (nombre, descripcion, precio, cantidad, categoria) VALUES (?, ?, ?, ?, ?)
    """
    try:
        #definimos la variable decisión y la iniciamos en "si", nos servirá para
        #utilizarla como corte del bucle while
        decision = "si"
        while decision.lower() == "si":

            #solicitamos los datos del producto a registrar
            nombre = input("Ingrese el nombre del producto: ")
            descripcion = input("Ingrese la descripción del producto: ")
            precio = validar_precio()
            cantidad = validar_stock()
            categoria = input("Ingrese la categoria del producto: ")

            cursor.execute(query, (nombre, descripcion, precio, cantidad, categoria))
            conexion.commit()
            
            #si el usuario ingresa "si", el programa volverá a solicitar los datos
            #para otro producto y se agregará en la lista de productos
            #en el caso que elija "no", se volverá al menú principal de opciones
            decision = input("¿Desea cargar otro producto a la lista? si/no: ")
            print("- -"*25)
        print("Registro/s guardado/s")
        print("-"*50)
    except sqlite3.Error as e:
        print(f"Error al guardar el registro: {e}\n")
    finally:
        conexion.close()

# ---------------------------------------------------------------------------- #
#                               ACTUALIZAR REGISTROS                           #
# ---------------------------------------------------------------------------- #
def actualizar():
    #le pedimos al usuario que ingrese el id de un producto que desea actualizar
    id_producto = int(input("Ingrese el ID del producto: "))
    
    #establecemos la conexion con la base de datos
    cursor, conexion = enlace_conexion()
    
    try:
        #ejecutamos una consulta para obtener el producto con el id proporcionado por el usuario
        #guardamos los resultados de ese solo registro con fetchone (si es que lo hay)
        cursor.execute("SELECT * FROM Productos WHERE id_producto = ?", (id_producto,))
        resultados = cursor.fetchone()
        
        #verificamos si no hay productos con el id proporcionado
        if not resultados:
            print("No hay productos cargados con el ID solicitado\n")
            return
        else:
            #si hay productos los mostramos en pantalla invocando la funcion mostrar_coincidencias y le pasamos
            #como argumento los resultados de la busqueda para que el usuario pueda ver el producto que va a modificar
            mostrar_coincidencias([resultados])
        
        #validamos que la cantidad a modificar sea correcta
        cantidad = validar_stock()
        
        #una vez validada la cantidad, hacemos la la consulta para modificar el producto seleccionado
        query = "UPDATE Productos SET cantidad = ? WHERE id_producto = ?"
        nuevos_valores = (cantidad, id_producto)
        
        #ejecutamos la consulta y los nuevos valores ingresados para la actualización del producto
        cursor.execute(query, nuevos_valores)
        #confirmamos los cambios realizados en la base de datos
        conexion.commit()
        print("Registro actualizado\n")
    
    except sqlite3.Error as e:
        #maneja cualquier error que pueda ocurri en la actualización
        print(f"Error al actualizar el registro: {e}\n")
    
    finally:
        conexion.close()

# ---------------------------------------------------------------------------- #
#                                ELIMINAR REGISTROS                            #
# ---------------------------------------------------------------------------- #
def eliminar():
    # le pedimos al usuario que ingrese el id del producto que desea eliminar
    id_producto = int(input("Ingrese el ID del producto que desea eliminar: "))
    
    # establecemos la conexión a la base de datos
    cursor, conexion = enlace_conexion()
    
    try:
        # ejecutamos una consulta para seleccionar el producto con el id proporcionado
        cursor.execute("SELECT * FROM Productos WHERE id_producto = ?", (id_producto,))
        resultados = cursor.fetchone()
        
        # verificamos si no se encontraron productos con el id proporcionado
        if not resultados:
            print("No existen registros con el ID proporcionado\n")
        else:
            #si hay productos los mostramos en pantalla invocando la funcion mostrar_coincidencias y le pasamos
            #como argumento los resultados de la busqueda para que el usuario pueda ver el producto que va a eliminar
            mostrar_coincidencias([resultados])
            
            # solicitamos la confirmación del usuario para eliminar el registro
            decision = input("Si está seguro/a de eliminar el registro ingrese SI, de lo contrario pulse ENTER: ")
            if decision.lower() == "si":
                query = "DELETE FROM Productos WHERE id_producto = ?"
                
                try:
                    # se ejecuta la consulta de eliminación con el id proporcionado
                    cursor.execute(query, (id_producto,))
                    #confirmamos los cambios realizados en la base de datos
                    conexion.commit()
                    print("Registro eliminado con éxito\n")
                except sqlite3.Error as e:
                    # maneja cualquier error que pueda ocurrir durante la eliminación
                    print(f"Error al eliminar el registro: {e}\n")
            else:
                print("El registro no ha sido eliminado\n")
    
    finally:
        conexion.close()


# ---------------------------------------------------------------------------- #
#                                CONSULTAR REGISTROS                           #
# ---------------------------------------------------------------------------- #
def consulta():
    cursor, conexion = enlace_conexion()
    cursor.execute("SELECT * FROM Productos")

    resultados = cursor.fetchall()

    if not resultados:
        print("No hay datos para mostrar\n")
    else:
        mostrar_coincidencias(resultados)
    conexion.close()

# ---------------------------------------------------------------------------- #
#                    CONSULTAR POR UN REGISTRO EN PARTICULAR                   #
# ---------------------------------------------------------------------------- #
def consulta_particular():
    id_producto = int(input("Ingrese el ID del producto que desea consultar: "))
    cursor, conexion = enlace_conexion()
    cursor.execute("SELECT * FROM Productos WHERE id_producto = ?", (id_producto,))

    resultados = cursor.fetchone()

    if not resultados:
        print("No hay datos para mostrar\n")
    else:
        mostrar_coincidencias([resultados])
    conexion.close()

# ---------------------------------------------------------------------------- #
#                             REPORTE DE BAJO STOCK                            #
# ---------------------------------------------------------------------------- #
def reporte_de_bajo_stock():
    bajo_stock = int(input("Ingrese el valor a considerar como bajo stock para generar el reporte: "))
    cursor, conexion = enlace_conexion()

    try:
        cursor.execute("SELECT * FROM Productos WHERE cantidad <= ?", (bajo_stock,))
        resultados = cursor.fetchall()

        if resultados:
            print("Productos con bajo stock: ")
            mostrar_coincidencias(resultados)
        else:
            print("No hay productos con bajo stock\n")
    except sqlite3.Error as e:
        print(f"Ocurrió un error al generar el reporte: {e}\n")
    finally:
        conexion.close()

# ---------------------------------------------------------------------------- #
#                                     MENU                                     #
# ---------------------------------------------------------------------------- #
def menu():
    print("\t\tGESTIÓN DE PRODUCTOS")
    while True:
        #menú inicial
        opcion = input("Menú de opciones\n1-Cargar productos\n2-Listado completo de productos\n3-Consultar un producto en particular\n4-Modificar productos\n5-Reporte de bajo stock\n6-Eliminar\n7-Salir del programa\nSeleccione la opción deseada: ")

        #casteamos(convertimos) el string(cadena de carácteres) a entero para evaluar la opción elegida
        opcion_int = int(opcion)

        #depende la opción elegida entrará en un bloque específico
        if opcion_int == 1:
            print(f"Usted ha seleccionado la opción {opcion_int}: Cargar productos")
            insertar()

        elif opcion_int == 2:
            print(f"Usted ha seleccionado la opción {opcion_int}: Listado completo de productos")
            consulta()

        elif opcion_int == 3:
            print(f"Usted ha seleccionado la opción {opcion_int}: Consultar un producto en particular")
            consulta_particular()

        elif opcion_int == 4:
            print(f"Usted ha seleccionado la opción {opcion_int}: Modificar productos")
            actualizar()

        elif opcion_int == 5:
            print(f"Usted ha seleccionado la opción {opcion_int}: Reporte de Bajo Stock")
            reporte_de_bajo_stock()

        elif opcion_int == 6:
            print(f"Usted ha seleccionado la opción {opcion_int}: Eliminar")
            eliminar()

        #si se elige el número 7 saldremos del programa
        elif opcion_int == 7:  
            print(f"Usted ha seleccionado la opción {opcion_int}: Salir del Programa")
            break
        else:
            #opción default, si no se elige una opción del 1 al 7 se mostrará un aviso de
            #opción incorrecta y se solicitara ingresar una opción válida
            print("La opción elegida es incorrecta, intentalo de nuevo\n")

    print("Fin del programa")

# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #
def main():
    #invocamos a la funcion crear_inventario, si no existe lo crea
    crear_inventario()
    #invocamos al menú de opciones
    menu()

# ---------------------------------------------------------------------------- #
#                         INVOCACIÓN PROGRAMA PRINCIPAL                        #
# ---------------------------------------------------------------------------- #
main()