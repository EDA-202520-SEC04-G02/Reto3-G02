import time, csv
csv.field_size_limit(2147483647)

from datetime import datetime

from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.Tree import binary_search_tree as bst
from DataStructures.Map import map_linear_probing as mp 
from DataStructures.List import array_list as lt

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO DONE: Llama a las funciónes de creación de las estructuras de datos
    catalog = {
        "flights": lt.new_list(),                # Lista completa de vuelos
        "by_airline": mp.new_map(2000, 0.5),     # Mapa carrier -> lista de vuelos
        "by_dest": mp.new_map(2000, 0.5),        # Mapa dest -> lista de vuelos
        "by_date": {"root": None}                # Árbol RBT (inicializado manualmente)
    }
    return catalog

# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    
    # Iniciar medición de tiempo
    start = get_time()

    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for flight in reader:
            clean_flight = format_flight(flight)

            # Insertar vuelo en la lista general
            lt.add_last(catalog["flights"], clean_flight)

            # Indexar por aerolínea
            add_by_airline(catalog, clean_flight)

            # Indexar por aeropuerto destino
            add_by_dest(catalog, clean_flight)

            # Indexar por fecha
            add_by_date(catalog, clean_flight)

    # Detener medición de tiempo
    end = get_time()
    delta = delta_time(start, end)

    total = lt.size(catalog["flights"])

    return {
        "time_ms": delta,
        "total_flights": total
    }


# ==========================================================
# FORMATEO Y PREPROCESAMIENTO DE VUELOS
# ==========================================================

def format_flight(flight):
    """
    Limpia y agrega campos derivados a cada vuelo.
    """

    def safe_time(val):
        if not val:
            return None
        try:
            return datetime.strptime(val.strip(), "%H:%M")
        except ValueError:
            return None

    def calc_delay(real, sched):
        if not real or not sched:
            return 0
        real_dt = safe_time(real)
        sched_dt = safe_time(sched)
        if not real_dt or not sched_dt:
            return 0
        diff = (real_dt - sched_dt).total_seconds() / 60
        # Ajuste si cruza medianoche
        if diff < -720:  # más de 12h atrás
            diff += 1440
        elif diff > 720:  # más de 12h adelante
            diff -= 1440
        return diff

    # Cálculos derivados
    flight["dep_delay"] = calc_delay(flight.get("dep_time"), flight.get("sched_dep_time"))
    flight["arr_delay"] = calc_delay(flight.get("arr_time"), flight.get("sched_arr_time"))

    # Limpieza de numéricos
    try:
        flight["distance"] = float(flight["distance"]) if flight.get("distance") not in (None, "") else 0.0
    except (ValueError, TypeError):
        flight["distance"] = 0.0

    try:
        flight["air_time"] = float(flight["air_time"]) if flight.get("air_time") not in (None, "") else 0.0
    except (ValueError, TypeError):
        flight["air_time"] = 0.0

    # Normalización de fecha
    flight["date"] = flight.get("date") if flight.get("date") else "Unknown"

    return flight

# ==========================================================
# ÍNDICES DE BÚSQUEDA
# ==========================================================

def add_by_airline(catalog, flight):
    """
    Inserta un vuelo en el índice de aerolíneas.
    """
    code = flight.get("carrier")
    if code is None:
        code = "Unknown"
    entry = mp.get(catalog["by_airline"], code)
    if entry is None:
        flights_list = lt.new_list()
        mp.put(catalog["by_airline"], code, flights_list)
    else:
        flights_list = entry
    lt.add_last(flights_list, flight)


def add_by_dest(catalog, flight):
    """
    Inserta un vuelo en el índice de aeropuertos destino.
    """
    dest = flight.get("dest")
    if dest is None:
        dest = "Unknown"
    entry = mp.get(catalog["by_dest"], dest)
    if entry is None:
        flights_list = lt.new_list()
        mp.put(catalog["by_dest"], dest, flights_list)
    else:
        flights_list = entry
    lt.add_last(flights_list, flight)


def add_by_date(catalog, flight):
    """
    Inserta un vuelo en el árbol ordenado por fecha.
    """
    date_key = flight.get("date", "Unknown")
    entry = rbt.get(catalog["by_date"], date_key)
    if entry is None:
        flights_list = lt.new_list()
        rbt.put(catalog["by_date"], date_key, flights_list)
    else:
        flights_list = entry
    lt.add_last(flights_list, flight)

# Funciones de consulta sobre el catálogo


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
