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
    # TODO: Imprimir el resultado del requerimiento 1
    pass


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
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


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
