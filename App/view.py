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
    Carga los datos
    """
    #TOD DONE: Realizar la carga de datos
    flightsfile = data_dir + "flights_large.csv"  # Ajusta el nombre al archivo real del reto

    # Llamar a la función de lógica
    resultados = logic.load_data(control, flightsfile)

    # Mostrar resultados
    print("\n=== Resultados de la carga de datos ===")
    print(f"Tiempo de carga: {resultados['time_ms']:.2f} ms")
    print(f"Total de vuelos cargados: {resultados['total_flights']}")

    # Preview de los primeros y últimos vuelos
    print("\nPrimeros y últimos 5 vuelos:")
    preview = get_preview(control["flights"], 5)
    headers = ["date", "carrier", "origin", "dest", "dep_delay", "arr_delay", "distance"]
    table = [[p.get(h, '') for h in headers] for p in preview]
    print(tabulate(table, headers=headers, tablefmt="grid"))

    return resultados

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

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO DONE: Imprimir el resultado del requerimiento 1

    airline = input("Ingrese el código de la aerolínea (ej: UA, DL, AA): ").strip().upper()
    min_delay = float(input("Ingrese el retraso mínimo (en minutos): "))
    max_delay = float(input("Ingrese el retraso máximo (en minutos): "))

    result = logic.req_1(control, airline, min_delay, max_delay)

    print("\n=== Requerimiento 1 ===")
    print(f"Aerolínea: {airline}")
    print(f"Tiempo de ejecución: {result['time_ms']:.2f} ms")
    print(f"Total de vuelos en el rango: {result['total_in_range']}")
    print(f"Retraso entre {min_delay} y {max_delay} minutos")

    flights = sl_to_arraylist(result["flights"])
    total = result["total_in_range"]

    if total == 0:
        print("No se encontraron vuelos en el rango especificado.")
        return

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

    # Preparar tabla
    headers = ["flight", "date", "carrier", "name", "origin", "dest", "dep_delay"]
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
            f.get("dep_delay", 0)
        ])

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
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

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

        elif int(inputs) == 5:
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
