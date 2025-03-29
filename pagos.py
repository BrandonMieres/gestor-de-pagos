import datetime
import csv
import os

# Carpeta y archivo para almacenar los datos
DATA_DIR = "datos"
DATA_FILE = os.path.join(DATA_DIR, "clientes.csv")

# Diccionario global para almacenar clientes
clientes = {}

# Variable global para IDs únicos
next_id = 1

def ensure_data_dir():
    """Crea la carpeta 'datos' si no existe."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def parse_fecha(fecha_str):
    """Convierte una cadena en formato dd/mm/aaaa a un objeto datetime."""
    try:
        return datetime.datetime.strptime(fecha_str, "%d/%m/%Y")
    except ValueError:
        return None

def formatear_fecha(fecha):
    """Devuelve una fecha formateada en dd/mm/aaaa."""
    return fecha.strftime("%d/%m/%Y")

def sumar_un_mes(fecha):
    """Suma un mes a la fecha dada, ajustando el día si es necesario."""
    new_month = fecha.month + 1 if fecha.month < 12 else 1
    new_year = fecha.year if fecha.month < 12 else fecha.year + 1
    try:
        return fecha.replace(month=new_month, year=new_year)
    except ValueError:
        # Ajusta al día 28 en caso de error (por ejemplo, al pasar de 31 de enero a febrero)
        return fecha.replace(day=28, month=new_month, year=new_year)

def get_yes_no_input(prompt):
    """Obtiene una entrada s/n del usuario, con 's' como valor por defecto si se deja vacío."""
    response = input(prompt).strip().lower()
    if response == "":
        return "s"
    return response

def load_data():
    """Carga los datos desde el archivo CSV al diccionario clientes."""
    global next_id, clientes
    clientes.clear()
    next_id = 1

    if not os.path.exists(DATA_FILE):
        return

    try:
        with open(DATA_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                id_cliente = int(row["id"])
                clientes[id_cliente] = {
                    "nombre": row["nombre"],
                    "fecha_inicio": parse_fecha(row["fecha_inicio"]),
                    "fecha_proximo": parse_fecha(row["fecha_proximo"]),
                    "monto": float(row["monto"]),
                    "descripcion": row["descripcion"]
                }
                # Actualizar next_id para que sea mayor al ID más grande
                if id_cliente >= next_id:
                    next_id = id_cliente + 1
    except Exception as e:
        print(f"Error al cargar datos: {e}")

def save_data():
    """Guarda los datos del diccionario clientes en el archivo CSV."""
    ensure_data_dir()
    try:
        with open(DATA_FILE, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["id", "nombre", "fecha_inicio", "fecha_proximo", "monto", "descripcion"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for id_cliente, info in clientes.items():
                writer.writerow({
                    "id": id_cliente,
                    "nombre": info["nombre"],
                    "fecha_inicio": formatear_fecha(info["fecha_inicio"]),
                    "fecha_proximo": formatear_fecha(info["fecha_proximo"]),
                    "monto": info["monto"],
                    "descripcion": info["descripcion"]
                })
    except Exception as e:
        print(f"Error al guardar datos: {e}")

def añadir_cliente():
    """Añade un cliente con opciones para elegir fechas automáticamente o ingresarlas manualmente."""
    global next_id
    print("\n--- Añadir Cliente ---")
    print("En cualquier momento, ingrese '0' o 'salir' para cancelar sin guardar.")

    # Nombre del cliente
    nombre = input("Ingrese el nombre del cliente: ").strip()
    if nombre.lower() in ["0", "salir"]:
        print("Operación cancelada.")
        return
    if not nombre:
        print("El nombre no puede estar vacío.")
        return

    # Fecha del primer pago
    usar_fecha_actual = get_yes_no_input("¿Usar la fecha actual como primer pago? (s/n, por defecto s): ")
    if usar_fecha_actual in ["0", "salir"]:
        print("Operación cancelada.")
        return
    if usar_fecha_actual == 's':
        fecha_inicio = datetime.datetime.today()
    else:
        fecha_inicio_str = input("Ingrese la fecha del primer pago (dd/mm/aaaa): ").strip()
        if fecha_inicio_str.lower() in ["0", "salir"]:
            print("Operación cancelada.")
            return
        fecha_inicio = parse_fecha(fecha_inicio_str)
        if not fecha_inicio:
            print("Fecha inválida. Intente nuevamente.")
            return

    # Fecha del próximo pago
    usar_mes_siguiente = get_yes_no_input("¿El próximo pago será en un mes? (s/n, por defecto s): ")
    if usar_mes_siguiente in ["0", "salir"]:
        print("Operación cancelada.")
        return
    if usar_mes_siguiente == 's':
        fecha_proximo = sumar_un_mes(fecha_inicio)
    else:
        fecha_proximo_str = input("Ingrese la fecha del próximo pago (dd/mm/aaaa): ").strip()
        if fecha_proximo_str.lower() in ["0", "salir"]:
            print("Operación cancelada.")
            return
        fecha_proximo = parse_fecha(fecha_proximo_str)
        if not fecha_proximo:
            print("Fecha inválida. Intente nuevamente.")
            return

    # Monto del pago mensual
    monto_input = input("Ingrese el monto del pago mensual: ").strip()
    if monto_input.lower() in ["0", "salir"]:
        print("Operación cancelada.")
        return
    try:
        monto = float(monto_input)
    except ValueError:
        print("Monto inválido. Debe ser un número.")
        return

    # Descripción
    descripcion = input("Ingrese una descripción del cliente: ").strip()
    if descripcion.lower() in ["0", "salir"]:
        print("Operación cancelada.")
        return

    # Si todo está bien, se añade el cliente
    id_cliente = next_id
    next_id += 1

    clientes[id_cliente] = {
        "nombre": nombre,
        "fecha_inicio": fecha_inicio,
        "fecha_proximo": fecha_proximo,
        "monto": monto,
        "descripcion": descripcion
    }
    save_data()  # Guardar datos después de añadir
    print(f"\nCliente añadido con éxito. ID asignado: {id_cliente}")
    print(f"Primer pago: {formatear_fecha(fecha_inicio)}")
    print(f"Próximo pago: {formatear_fecha(fecha_proximo)}")

def editar_cliente():
    """
    Muestra una lista de clientes, solicita el ID del cliente a editar y pregunta
    si desea editar o borrar el cliente. Si se edita, permite modificar nombre,
    cantidad a pagar, descripción o fechas de pago. Si se borra, elimina el cliente.
    """
    print("\n--- Editar Cliente ---")
    print("En cualquier momento, ingrese '0' o 'salir' para cancelar sin guardar.")
    if not clientes:
        print("No hay clientes registrados.")
        return

    # Mostrar lista de clientes
    print("Lista de clientes:")
    for id_cliente, info in clientes.items():
        print(f"ID: {id_cliente} | Nombre: {info['nombre']}")
    
    id_input = input("Ingrese el ID del cliente a editar: ").strip()
    if id_input.lower() in ["0", "salir"]:
        print("Operación cancelada.")
        return
    try:
        id_seleccionado = int(id_input)
    except ValueError:
        print("ID inválido.")
        return

    if id_seleccionado not in clientes:
        print("No existe un cliente con ese ID.")
        return

    cliente = clientes[id_seleccionado]
    print(f"\nCliente seleccionado: {cliente['nombre']}")
    print("¿Qué desea hacer?")
    print("1. Editar cliente")
    print("2. Borrar cliente")
    print("0. Cancelar")
    accion = input("Seleccione una opción (0-2): ").strip()

    if accion.lower() in ["0", "salir"]:
        print("Operación cancelada.")
        return
    elif accion == "2":
        confirmacion = get_yes_no_input(f"¿Está seguro de que desea borrar al cliente {cliente['nombre']}? (s/n, por defecto s): ")
        if confirmacion == "s":
            del clientes[id_seleccionado]
            save_data()  # Guardar datos después de borrar
            print(f"Cliente {cliente['nombre']} borrado con éxito.")
        else:
            print("Operación cancelada.")
        return
    elif accion != "1":
        print("Opción no válida.")
        return

    # Proceder con la edición
    while True:
        print(f"\nEditando cliente: {cliente['nombre']}")
        print("¿Qué desea modificar?")
        print("1. Nombre")
        print("2. Cantidad a pagar")
        print("3. Descripción")
        print("4. Fechas de pago")
        print("0. Salir de edición")
        opcion = input("Seleccione una opción (0-4): ").strip()

        if opcion.lower() in ["0", "salir"]:
            print("Saliendo del modo de edición.")
            break
        elif opcion == "1":
            nuevo_nombre = input("Ingrese el nuevo nombre: ").strip()
            if nuevo_nombre.lower() in ["0", "salir"]:
                print("Modificación cancelada.")
                continue
            if nuevo_nombre:
                cliente["nombre"] = nuevo_nombre
                save_data()  # Guardar datos después de modificar
                print("Nombre actualizado con éxito.")
            else:
                print("El nombre no puede estar vacío.")
        elif opcion == "2":
            monto_input = input("Ingrese la nueva cantidad a pagar: ").strip()
            if monto_input.lower() in ["0", "salir"]:
                print("Modificación cancelada.")
                continue
            try:
                nuevo_monto = float(monto_input)
                cliente["monto"] = nuevo_monto
                save_data()  # Guardar datos después de modificar
                print("Monto actualizado con éxito.")
            except ValueError:
                print("Monto inválido.")
        elif opcion == "3":
            nueva_descripcion = input("Ingrese la nueva descripción: ").strip()
            if nueva_descripcion.lower() in ["0", "salir"]:
                print("Modificación cancelada.")
                continue
            cliente["descripcion"] = nueva_descripcion
            save_data()  # Guardar datos después de modificar
            print("Descripción actualizada con éxito.")
        elif opcion == "4":
            print("¿Qué fecha desea modificar?")
            print("1. Fecha del primer pago")
            print("2. Fecha del próximo pago")
            sub_opcion = input("Seleccione una opción (1-2, o '0' para cancelar): ").strip()
            if sub_opcion.lower() in ["0", "salir"]:
                print("Modificación cancelada.")
                continue
            if sub_opcion == "1":
                nueva_fecha_str = input("Ingrese la nueva fecha del primer pago (dd/mm/aaaa): ").strip()
                if nueva_fecha_str.lower() in ["0", "salir"]:
                    print("Modificación cancelada.")
                    continue
                nueva_fecha = parse_fecha(nueva_fecha_str)
                if nueva_fecha:
                    cliente["fecha_inicio"] = nueva_fecha
                    print("Fecha del primer pago actualizada con éxito.")
                    # Al editar el primer pago, se debe actualizar también el próximo pago
                    ajustar = get_yes_no_input("¿Desea que el próximo pago sea automáticamente el mes siguiente? (s/n, por defecto s): ")
                    if ajustar in ["0", "salir"]:
                        print("Modificación cancelada.")
                        continue
                    if ajustar == "s":
                        cliente["fecha_proximo"] = sumar_un_mes(nueva_fecha)
                        print("Fecha del próximo pago actualizada automáticamente.")
                    else:
                        nueva_fecha_proximo_str = input("Ingrese la nueva fecha del próximo pago (dd/mm/aaaa): ").strip()
                        if nueva_fecha_proximo_str.lower() in ["0", "salir"]:
                            print("Modificación cancelada.")
                            continue
                        nueva_fecha_proximo = parse_fecha(nueva_fecha_proximo_str)
                        if nueva_fecha_proximo:
                            cliente["fecha_proximo"] = nueva_fecha_proximo
                            print("Fecha del próximo pago actualizada con éxito.")
                        else:
                            print("Fecha inválida para el próximo pago. No se actualizó.")
                    save_data()  # Guardar datos después de modificar fechas
                else:
                    print("Fecha inválida.")
            elif sub_opcion == "2":
                nueva_fecha_str = input("Ingrese la nueva fecha del próximo pago (dd/mm/aaaa): ").strip()
                if nueva_fecha_str.lower() in ["0", "salir"]:
                    print("Modificación cancelada.")
                    continue
                nueva_fecha = parse_fecha(nueva_fecha_str)
                if nueva_fecha:
                    cliente["fecha_proximo"] = nueva_fecha
                    save_data()  # Guardar datos después de modificar
                    print("Fecha del próximo pago actualizada con éxito.")
                else:
                    print("Fecha inválida.")
            else:
                print("Opción no válida para fechas.")
        else:
            print("Opción no válida.")

def gestionar_pagos():
    """Muestra la información de los pagos programados, permite gestionar pagos por cliente y visualizar pagos por mes."""
    print("\n--- Gestión de Pagos ---")
    if not clientes:
        print("No hay clientes registrados.")
        return
    
    while True:
        print("\nOpciones:")
        print("1. Gestionar pago de un cliente")
        print("2. Visualizar pagos por mes")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción (1-3): ").strip()

        if opcion == "1":
            # Mostrar lista de clientes
            print("\nLista de clientes:")
            for id_cliente, info in clientes.items():
                print(f"ID: {id_cliente} | Nombre: {info['nombre']} | Próximo pago: {formatear_fecha(info['fecha_proximo'])}")

            # Solicitar ID del cliente
            id_input = input("\nIngrese el ID del cliente a gestionar (o '0' para volver atrás): ").strip()
            if id_input.lower() in ["0", "salir"]:
                continue
            
            try:
                id_seleccionado = int(id_input)
            except ValueError:
                print("ID inválido.")
                continue

            if id_seleccionado not in clientes:
                print("No existe un cliente con ese ID.")
                continue

            # Mostrar información del cliente seleccionado
            cliente = clientes[id_seleccionado]
            print(f"\nCliente seleccionado: {cliente['nombre']}")
            print(f"Monto a pagar mensualmente: ${cliente['monto']:.2f}")
            print(f"Primer pago: {formatear_fecha(cliente['fecha_inicio'])}")
            print(f"Próximo pago: {formatear_fecha(cliente['fecha_proximo'])}")

            # Submenú para gestionar el pago
            print("\nOpciones para el cliente:")
            print("1. Cliente pagado (actualiza el próximo pago un mes más)")
            print("2. Volver atrás")
            sub_opcion = input("Seleccione una opción (1-2): ").strip()

            if sub_opcion == "1":
                cliente["fecha_proximo"] = sumar_un_mes(cliente["fecha_proximo"])
                save_data()  # Guardar los cambios en el archivo CSV
                print(f"Pago registrado. Nuevo próximo pago: {formatear_fecha(cliente['fecha_proximo'])}")
            elif sub_opcion == "2" or sub_opcion.lower() in ["0", "salir"]:
                continue
            else:
                print("Opción no válida.")

        elif opcion == "2":
            # Submenú para visualizar pagos
            hoy = datetime.datetime.today()
            mes_actual = hoy.month
            año_actual = hoy.year
            proximo_mes = mes_actual + 1 if mes_actual < 12 else 1
            proximo_año = año_actual if mes_actual < 12 else año_actual + 1

            print("\nOpciones de visualización:")
            print(f"1. Ver ganancias de este mes ({mes_actual:02d}/{año_actual})")
            print(f"2. Ver ganancias del próximo mes ({proximo_mes:02d}/{proximo_año})")
            print("3. Ingresar fecha manualmente")
            print("4. Volver atrás")
            sub_opcion = input("Seleccione una opción (1-4): ").strip()

            if sub_opcion == "1":
                mes, año = mes_actual, año_actual
            elif sub_opcion == "2":
                mes, año = proximo_mes, proximo_año
            elif sub_opcion == "3":
                mes_input = input("\nIngrese el mes y año a visualizar (mm/aaaa): ").strip()
                if mes_input.lower() in ["0", "salir"]:
                    continue
                try:
                    mes, año = map(int, mes_input.split("/"))
                    if not (1 <= mes <= 12 and 2000 <= año <= 9999):
                        raise ValueError
                except ValueError:
                    print("Formato inválido. Use mm/aaaa (ejemplo: 03/2025).")
                    continue
            elif sub_opcion == "4" or sub_opcion.lower() in ["0", "salir"]:
                continue
            else:
                print("Opción no válida.")
                continue

            # Filtrar clientes con pagos en el mes seleccionado
            total_mes = 0.0
            pagos_mes = []
            for id_cliente, info in clientes.items():
                fecha_proximo = info["fecha_proximo"]
                if fecha_proximo.month == mes and fecha_proximo.year == año:
                    pagos_mes.append((id_cliente, info["nombre"], info["monto"]))
                    total_mes += info["monto"]

            # Mostrar resultados
            if pagos_mes:
                print(f"\nPagos programados para {mes:02d}/{año}:")
                for id_cliente, nombre, monto in pagos_mes:
                    print(f"ID: {id_cliente} | Nombre: {nombre} | Monto: ${monto:.2f}")
                print(f"\nTotal a ganar en {mes:02d}/{año}: ${total_mes:.2f}")
            else:
                print(f"No hay pagos programados para {mes:02d}/{año}.")

        elif opcion == "3" or opcion.lower() in ["0", "salir"]:
            print("Volviendo al menú principal.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

def mostrar_menu():
    """Muestra el menú principal del programa."""
    print("\n==== MENÚ PRINCIPAL ====")
    print("1. Añadir Cliente")
    print("2. Editar Cliente")
    print("3. Gestionar Pagos")
    print("4. Salir")

def main():
    """Ejecuta el programa y gestiona el menú principal."""
    load_data()  # Cargar datos al inicio
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            añadir_cliente()
        elif opcion == "2":
            editar_cliente()
        elif opcion == "3":
            gestionar_pagos()
        elif opcion == "4":
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()