import sys

import App.logic as logic
from tabulate import tabulate 
import os
data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'
from DataStructures.List import array_list as lt


def new_logic():
    """
        Se crea una instancia del controlador
    """
    #TODO DONE: Llamar la función de la lógica donde se crean las estructuras de datos
    control = logic.new_logic()
    return control

def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control):
    """
    Vista: solicita archivo, llama a logic.load_data() y muestra los resultados.
    """
    print("\n=== CARGA DE DATOS ===")

    file_path = data_dir + "flights_large.csv"

    result = logic.load_data(control, file_path)

    print(f"\nTiempo de carga: {result['time']} ms")
    print(f"Total de vuelos cargados: {result['total']}\n")

    print("Primeros 5 vuelos:")
    print_flight_table(result["first5"])
    print("\nÚltimos 5 vuelos:")
    print_flight_table(result["last5"])


def print_flight_table(flights):
    headers = [
        "Fecha", "Hora Salida Real", "Hora Llegada Real",
        "Hora Salida Prog.", "Hora Llegada Prog.",
        "Código Aerolínea", "Nombre Aerolínea", "Identificador Aeronave",
        "Origen", "Destino",
        "Duración (min)", "Distancia (mi)",
        "Retraso Salida (min)", "Retraso Llegada (min)"
    ]

    table = []
    size = lt.size(flights)

    for i in range(size):
        f = lt.get_element(flights, i)
        row = [
            f["date"],
            f["dep_time"] or "Unknown",
            f["arr_time"] or "Unknown",
            f["sched_dep_time"] or "Unknown",
            f["sched_arr_time"] or "Unknown",
            f["carrier"],
            f["name"],
            f["tailnum"],
            f["origin"],
            f["dest"],
            f["duration"],
            f["distance"],
            f["dep_delay"],
            f["arr_delay"]
        ]
        table.append(row)

    print(tabulate(table, headers=headers, tablefmt="grid"))





'''
def load_data(control):
    flightsfile = data_dir + "flights_large.csv"
    resultados = logic.load_data(control, flightsfile)

    print("\n=== Resultados de la carga de datos ===")
    print(f"Tiempo de carga: {resultados['time_ms']:.2f} ms")
    print(f"Total de vuelos cargados: {resultados['total_flights']}")

    print("\nPrimeros y últimos 5 vuelos:")
    preview = get_preview(resultados["preview"], 5)
    headers = ["date", "sched_dep_time", "arr_time", "carrier", "name", "tailnum",
               "origin", "dest", "air_time", "distance"]
    table = [[p.get(h, 'Unknown') for h in headers] for p in preview]
    print(tabulate(table, headers=headers, tablefmt="grid"))


def get_preview(flights_list, n):
    """
    Retorna los primeros y últimos n vuelos de la lista.
    """
    #TODO: Realizar la función para imprimir un elemento
    total = logic.lt.size(flights_list)
    preview = logic.lt.new_list()  # lista propia de nuestra estructura

    # Primeros n elementos
    limit = n if n < total else total
    for i in range(0, limit):  # 0-based
        elem = logic.lt.get_element(flights_list, i)
        logic.lt.add_last(preview, elem)

    # Últimos n elementos (solo si hay más de n)
    if total > n:
        start = total - n
        for i in range(start, total):  # 0-based
            elem = logic.lt.get_element(flights_list, i)
            logic.lt.add_last(preview, elem)

    # Convertir la lista de nuestra estructura a una lista de Python para tabulate
    result = []
    for i in range(0, logic.lt.size(preview)):
        result.append(logic.lt.get_element(preview, i))

    return result
'''


def print_req_1(control):
    """5
    Requerimiento 1:
    Dada una aerolínea, listar los vuelos con retraso de salida dentro de un rango específico de minutos.
    """
    print("\n=== Requerimiento 1: Retrasos por Aerolínea ===")

    # Entrada de parámetros
    code = input("Ingrese el código de la aerolínea (ej: 'UA'): ").strip().upper()
    min_d = int(input("Ingrese el retraso mínimo (en minutos): "))
    max_d = int(input("Ingrese el retraso máximo (en minutos): "))

    # Llamado al controlador
    result = logic.req_1(control, code, min_d, max_d)

    print(f"\nTiempo de ejecución: {result['time']} ms")
    print(f"Total de vuelos con retraso dentro del rango: {result['total']}")

    if result["total"] == 0:
        print("No se encontraron vuelos en ese rango para la aerolínea seleccionada.")
        return

    # =====================
    # Tabla: primeros 5 vuelos
    # =====================
    print("\nPrimeros 5 vuelos:")
    headers = [
        "ID", "Código Vuelo", "Fecha",
        "Nombre Aerolínea", "Código Aerolínea",
        "Origen", "Destino", "Retraso Salida (min)"
    ]
    table = []
    size = lt.size(result["first5"])

    for i in range(size):
        f = lt.get_element(result["first5"], i)
        row = [
            f["id"],
            f["flight"],
            f["date"],
            f["name"],
            f["carrier"],
            f["origin"],
            f["dest"],
            f["dep_delay"]
        ]
        table.append(row)

    print(tabulate(table, headers=headers, tablefmt="grid"))

    # =====================
    # Tabla: últimos 5 vuelos
    # =====================
    print("\nÚltimos 5 vuelos:")
    table = []
    size = lt.size(result["last5"])

    for i in range(size):
        f = lt.get_element(result["last5"], i)
        row = [
            f["id"],
            f["flight"],
            f["date"],
            f["name"],
            f["carrier"],
            f["origin"],
            f["dest"],
            f["dep_delay"]
        ]
        table.append(row)

    print(tabulate(table, headers=headers, tablefmt="grid"))


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    carrier = input("Ingrese el código de la aerolínea (ej: AA, UA, DL): ").strip().upper()
    dest = input("Ingrese el código del aeropuerto destino (ej: JFK, LAX): ").strip().upper()
    min_dist = float(input("Ingrese la distancia mínima (en millas): "))
    max_dist = float(input("Ingrese la distancia máxima (en millas): "))

    result = logic.req_3(control, carrier, dest, min_dist, max_dist)

    print("\n=== Requerimiento 3 ===")
    print(f"Aerolínea: {carrier} | Destino: {dest}")
    print(f"Rango de distancia: {min_dist} - {max_dist} millas")
    print(f"Tiempo de ejecución: {result['time_ms']:.2f} ms")
    print(f"Total de vuelos en el rango: {result['total_in_range']}")

    flights = result["flights"]
    total = result["total_in_range"]

    if total == 0:
        print("No se encontraron vuelos en el rango especificado.")
        return

    # Convertir de single_linked_list a array_list
    flights = sl_to_arraylist(flights)

    # Mostrar los 5 primeros y 5 últimos vuelos si hay más de 10
    limit = 5
    flights_to_show = lt.new_list()

    if total <= 10:
        flights_to_show = flights
    else:
        # Agregar los primeros 5
        for i in range(0, limit):
            lt.add_last(flights_to_show, lt.get_element(flights, i))
        # Agregar los últimos 5
        for i in range(total - limit, total):
            lt.add_last(flights_to_show, lt.get_element(flights, i))

    # Preparar tabla para imprimir
    headers = ["flight", "date", "carrier", "name", "origin", "dest", "distance"]
    table = []

    for i in range(0, lt.size(flights_to_show)):
        f = lt.get_element(flights_to_show, i)
        table.append([
            f.get("flight", ""),
            f.get("date", ""),
            f.get("carrier", ""),
            f.get("name", ""),
            f.get("origin", ""),
            f.get("dest", ""),
            f.get("distance", 0)
        ])

    print(tabulate(table, headers=headers, tablefmt="grid"))

def print_req_4(control):
    """
    Imprime los resultados del Requerimiento 4:
    Top N aerolíneas con más vuelos en rango de fechas y horas.
    """
    # TODO DONE: Imprimir el resultado del requerimiento 4

    date_start = input("Ingrese la fecha inicial (YYYY-MM-DD): ").strip()
    date_end = input("Ingrese la fecha final (YYYY-MM-DD): ").strip()
    time_start = input("Ingrese la hora inicial (HH:MM): ").strip()
    time_end = input("Ingrese la hora final (HH:MM): ").strip()
    top_n = int(input("Ingrese la cantidad N de aerolíneas a mostrar: "))

    result = logic.req_4(control, date_start, date_end, time_start, time_end, top_n)

    print("\n=== Requerimiento 4 ===")
    print(f"Rango de fechas: {date_start} a {date_end}")
    print(f"Franja horaria: {time_start} - {time_end}")
    print(f"Tiempo de ejecución: {result['time_ms']:.2f} ms")
    print(f"N aerolíneas consideradas: {result['total_airlines']}")

    airlines = result["top_airlines"]

    if lt.size(airlines) == 0:
        print("No se encontraron vuelos en el rango especificado.")
        return

    headers = [
        "carrier", "total_vuelos", "prom_duracion", "prom_distancia",
        "min_flight_id", "min_flight_date", "min_flight_sched", "origin", "dest", "duracion"
    ]
    table = []

    for i in range(0, lt.size(airlines)):
        a = lt.get_element(airlines, i)
        min_f = a["min_flight"]
        table.append([
            a["carrier"],
            a["total_vuelos"],
            round(a["prom_duracion"], 2),
            round(a["prom_distancia"], 2),
            min_f.get("id", ""),
            min_f.get("date", ""),
            min_f.get("sched_dep_time", ""),
            min_f.get("origin", ""),
            min_f.get("dest", ""),
            min_f.get("air_time", "")
        ])

    print(tabulate(table, headers=headers, tablefmt="grid"))


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    
    
    date_start = input("Ingrese la fecha inicial (YYYY-MM-DD): ").strip()
    date_end = input("Ingrese la fecha final (YYYY-MM-DD): ").strip()
    dest_code = input("Ingrese el código del aeropuerto de destino (ej: JFK, LAX): ").strip().upper()
    top_n = int(input("Ingrese la cantidad N de aerolíneas más puntuales a mostrar: "))


    result = logic.req_5(control, date_start, date_end, dest_code, top_n)

    print("\n=== Requerimiento 5 ===")
    print(f"Rango de fechas: {date_start} a {date_end}")
    print(f"Aeropuerto de destino: {dest_code}")
    print(f"Tiempo de ejecución: {result['time_ms']:.2f} ms")
    print(f"N aerolíneas retornadas: {result['total_airlines']}")

    airlines = result["airlines"]

    if lt.size(airlines) == 0:
        print("No se encontraron vuelos que cumplan las condiciones.")
        return

    headers = [
        "Aerolínea",
        "Total vuelos",
        "Duración prom. (min)",
        "Distancia prom. (mi)",
        "Puntualidad prom. llegada (min)",
        "ID vuelo máx. distancia",
        "Código vuelo",
        "Fecha llegada",
        "Hora llegada",
        "Origen",
        "Destino",
        "Duración vuelo (min)",
        "Distancia vuelo (mi)"
    ]

    table = []

    for i in range(0, lt.size(airlines)):
        a = lt.get_element(airlines, i)
        max_f = a["max_dist_flight"]

        fecha_llegada = max_f.get("date", "")
        hora_llegada = max_f.get("arr_time", "") or max_f.get("sched_arr_time", "")

        table.append([
            a.get("carrier", ""),
            a.get("total_vuelos", 0),
            round(a.get("avg_duration", 0.0), 2),
            round(a.get("avg_distance", 0.0), 2),
            round(a.get("avg_delay", 0.0), 2),
            max_f.get("id", ""),
            max_f.get("flight", ""),
            fecha_llegada,
            hora_llegada,
            max_f.get("origin", ""),
            max_f.get("dest", ""),
            round(max_f.get("duration", 0.0), 2),
            round(max_f.get("distance", 0.0), 2)
        ])

    print(tabulate(table, headers=headers, tablefmt="grid"))


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6

    date_start = input("Ingrese la fecha inicial (YYYY-MM-DD): ").strip()
    date_end = input("Ingrese la fecha final (YYYY-MM-DD): ").strip()
    min_dist = float(input("Ingrese la distancia mínima (en millas): "))
    max_dist = float(input("Ingrese la distancia máxima (en millas): "))
    top_m = int(input("Ingrese la cantidad M de aerolíneas más estables a mostrar: "))

    result = logic.req_6(control, date_start, date_end, min_dist, max_dist, top_m)

    print("\n=== Requerimiento 6 ===")
    print(f"Rango de fechas: {date_start} a {date_end}")
    print(f"Rango de distancias: {min_dist} - {max_dist} millas")
    print(f"Tiempo de ejecución: {result['time_ms']:.2f} ms")
    print(f"M aerolíneas retornadas: {result['total_airlines']}")

    airlines = result["airlines"]

    if lt.size(airlines) == 0:
        print("No se encontraron vuelos que cumplan las condiciones.")
        return

    
    headers = [
        "Aerolínea",
        "Total vuelos",
        "Prom. retraso/anticipo salida (min)",
        "Estabilidad salida (desv. estándar, min)",
        "ID vuelo representativo",
        "Código vuelo",
        "Fecha salida",
        "Hora salida",
        "Origen",
        "Destino",
        "Retraso vuelo (min)"
    ]

    table = []

    for i in range(0, lt.size(airlines)):
        a = lt.get_element(airlines, i)
        best_f = a["best_flight"]

        fecha_salida = best_f.get("date", "")
        hora_salida = best_f.get("dep_time", "") or best_f.get("sched_dep_time", "")

        table.append([
            a.get("carrier", ""),
            a.get("total_vuelos", 0),
            round(a.get("mean_delay", 0.0), 2),
            round(a.get("std_delay", 0.0), 2),
            best_f.get("id", ""),
            best_f.get("flight", ""),
            fecha_salida,
            hora_salida,
            best_f.get("origin", ""),
            best_f.get("dest", ""),
            round(best_f.get("dep_delay", 0.0), 2)
        ])

    print(tabulate(table, headers=headers, tablefmt="grid"))

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 6:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)

def sl_to_arraylist(sl_list):
    """
    Convierte una single_linked_list a un array_list.
    """
    arr = lt.new_list()
    node = sl_list["first"]
    while node is not None:
        lt.add_last(arr, node["info"])
        node = node["next"]
    return arr
