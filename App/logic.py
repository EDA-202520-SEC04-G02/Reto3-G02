import time, csv
csv.field_size_limit(2147483647)

from datetime import datetime

from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.Tree import binary_search_tree as bst
from DataStructures.Map import map_linear_probing as mp 
from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as sl


def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO DONE: Llama a las funciónes de creación de las estructuras de datos
    catalog = {
        "flights": lt.new_list(),                # Lista completa de vuelos
        "by_airline": mp.new_map(2000, 0.5),     # Mapa carrier -> lista de vuelos
        "by_dest": mp.new_map(2000, 0.5),        # Mapa dest -> lista de vuelos
        "by_date": {"root": None},                # Árbol RBT (inicializado manualmente)
        "by_airline_delay": mp.new_map(2000, 0.5), # Mapa carrier -> RBT de vuelos por delay
    }
    catalog["by_airline_dest_distance"] = mp.new_map(200, 0.5)
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
            
            add_by_airline_delay(catalog, clean_flight)
            add_by_airline_dest_distance(catalog, clean_flight)
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

def add_by_airline_dest_distance(catalog, flight):
    """
    Indexa un vuelo por (aerolínea -> destino -> distancia) en un mapa de mapas.
    Nivel 1: carrier (aerolínea)
    Nivel 2: destino
    Valor final: árbol RBT ordenado por (distance, fecha_hora_llegada)
    """
    carrier = flight.get("carrier")
    dest = flight.get("dest")
    distance = float(flight.get("distance", 0))

    if not carrier or not dest:
        return

    # Obtener mapa de destinos de la aerolínea
    airline_map = mp.get(catalog["by_airline_dest_distance"], carrier)
    if airline_map is None:
        airline_map = mp.new_map(100, 0.5)   # mapa interno de destinos
        mp.put(catalog["by_airline_dest_distance"], carrier, airline_map)

    # Obtener árbol del aeropuerto destino
    distance_tree = mp.get(airline_map, dest)
    if distance_tree is None:
        distance_tree = {"root": None}
        mp.put(airline_map, dest, distance_tree)

    # Clave ordenable: (distancia, fecha + hora llegada)
    key = (distance, f"{flight.get('date', '')}_{flight.get('arr_time', '')}")
    rbt.put(distance_tree, key, flight)


def add_by_airline_delay(catalog, flight):
    """
    Indexa un vuelo en el árbol de retrasos (dep_delay) de su aerolínea.
    Clave: (dep_delay, fecha_hora)
    Valor: diccionario completo del vuelo.
    """

    carrier = flight.get("carrier")
    delay = float(flight.get("dep_delay", 0))

    if carrier is None:
        return

    # Buscar o crear el árbol de la aerolínea
    delay_tree = mp.get(catalog["by_airline_delay"], carrier)
    if delay_tree is None:
        delay_tree = {"root": None}  # tu implementación de RBT no tiene new_tree()
        mp.put(catalog["by_airline_delay"], carrier, delay_tree)

    # Crear clave ordenable (retraso + fecha_hora para desempatar)
    key = (delay, f"{flight.get('date', '')}_{flight.get('dep_time', '')}")

    # Insertar el vuelo en el árbol
    rbt.put(delay_tree, key, flight)


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


def req_1(catalog, airline_code, min_delay, max_delay):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO DONE: Modificar el requerimiento 1
    start = get_time()

    delay_tree = mp.get(catalog["by_airline_delay"], airline_code)
    if delay_tree is None:
        end = get_time()
        return {
            "airline": airline_code,
            "total_in_range": 0,
            "flights": lt.new_list(),
            "time_ms": delta_time(start, end)
        }

    # Buscar los vuelos dentro del rango
    key_min = (min_delay, "")
    key_max = (max_delay, "zzz")
    flights_in_range = rbt.values(delay_tree, key_min, key_max)

    total = sl.size(flights_in_range)
    end = get_time()

    return {
        "airline": airline_code,
        "total_in_range": total,
        "flights": flights_in_range,
        "time_ms": delta_time(start, end)
    }


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass

def req_3(catalog, carrier, dest, min_dist, max_dist):
    """
    Dada una aerolínea y un aeropuerto de destino,
    retorna los vuelos dentro del rango de distancia especificado.
    """
    # TODO: Modificar el requerimiento 3

    start = get_time()

    airline_map = mp.get(catalog["by_airline_dest_distance"], carrier)
    if airline_map is None:
        end = get_time()
        return {
            "carrier": carrier,
            "dest": dest,
            "total_in_range": 0,
            "flights": lt.new_list(),
            "time_ms": delta_time(start, end)
        }

    distance_tree = mp.get(airline_map, dest)
    if distance_tree is None:
        end = get_time()
        return {
            "carrier": carrier,
            "dest": dest,
            "total_in_range": 0,
            "flights": lt.new_list(),
            "time_ms": delta_time(start, end)
        }

    # Buscar en el árbol de distancias
    key_min = (min_dist, "")
    key_max = (max_dist, "zzz")
    flights_in_range = rbt.values(distance_tree, key_min, key_max)

    total = sl.size(flights_in_range)
    end = get_time()

    return {
        "carrier": carrier,
        "dest": dest,
        "total_in_range": total,
        "flights": flights_in_range,
        "time_ms": delta_time(start, end)
    }

def req_4(catalog, date_start, date_end, time_start, time_end, top_n):
    """
    Requerimiento 4:
    Para un rango de fechas y franja horaria de salida,
    identificar las N aerolíneas con mayor número de vuelos
    y, de cada una, obtener el vuelo con menor duración.
    """
    # TOD DONE: Modificar el requerimiento 4

    start = get_time()

    # Convertir fechas y horas de entrada a objetos datetime
    date_start = datetime.strptime(date_start, "%Y-%m-%d")
    date_end = datetime.strptime(date_end, "%Y-%m-%d")

    def parse_hour(hstr):
        return datetime.strptime(hstr, "%H:%M").time()

    time_start = parse_hour(time_start)
    time_end = parse_hour(time_end)

    # Estructura de agregación por aerolínea
    mp_airlines = mp.new_map(200, 0.5)

    flights_list = catalog["flights"]

    for i in range(0, lt.size(flights_list)):
        flight = lt.get_element(flights_list, i)

        # Validar datos mínimos
        if not flight.get("date") or not flight.get("sched_dep_time"):
            continue

        # Parsear fecha y hora
        try:
            f_date = datetime.strptime(flight["date"], "%Y-%m-%d")
            f_time = datetime.strptime(flight["sched_dep_time"], "%H:%M").time()
        except Exception:
            continue

        # Filtrar por rango de fecha y hora
        if not (date_start <= f_date <= date_end):
            continue
        if not (time_start <= f_time <= time_end):
            continue

        carrier = flight.get("carrier")
        if not carrier:
            continue

        # Obtener duración (air_time) y distancia
        dur = float(flight.get("air_time", 0))
        dist = float(flight.get("distance", 0))

        # Buscar o crear entrada para la aerolínea
        record = mp.get(mp_airlines, carrier)
        if record is None:
            record = {
                "carrier": carrier,
                "total_vuelos": 0,
                "sum_duracion": 0.0,
                "sum_distancia": 0.0,
                "min_flight": None
            }
            mp.put(mp_airlines, carrier, record)

        # Actualizar agregados
        record["total_vuelos"] += 1
        record["sum_duracion"] += dur
        record["sum_distancia"] += dist

        # Actualizar vuelo mínimo
        min_f = record["min_flight"]
        if min_f is None or dur < float(min_f.get("air_time", 1e9)) or (
            dur == float(min_f.get("air_time", 1e9)) and flight["sched_dep_time"] < min_f["sched_dep_time"]
        ):
            record["min_flight"] = flight

    # Crear priority queue para ordenar por número de vuelos (desc)
    pq_top = pq.new_heap(is_min_pq=True)
    
    # Recorrer aerolíneas y agregarlas al heap
    for carrier in mp.key_set(mp_airlines)["elements"]:
        data = mp.get(mp_airlines, carrier)
        total = data["total_vuelos"]
        # Negar total para crear max-heap (la PQ tuya suele ser min-heap)
        pq.insert(pq_top, (-total, carrier), data)

    # Extraer las N primeras
    top_list = lt.new_list()
    count = 0
    while not pq.is_empty(pq_top) and count < top_n:
        data = pq.remove(pq_top)
        data["prom_duracion"] = data["sum_duracion"] / data["total_vuelos"]
        data["prom_distancia"] = data["sum_distancia"] / data["total_vuelos"]
        lt.add_last(top_list, data)
        count += 1

    end = get_time()
    delta = delta_time(start, end)

    return {
        "time_ms": delta,
        "top_airlines": top_list,
        "total_airlines": count
    }


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
