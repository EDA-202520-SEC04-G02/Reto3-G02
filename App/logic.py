import time, csv
csv.field_size_limit(2147483647)
import codecs
from datetime import datetime

from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.Tree import binary_search_tree as bst
from DataStructures.Map import map_linear_probing as mp 
from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as sl

import csv
import time
import datetime
import math

# ============================================================
# CREACIÓN DEL CATÁLOGO
# ============================================================

def new_logic():
    catalog = {
        "flights": lt.new_list(),
        "by_date": rbt.new_map(),     # YYYY-MM-DD -> lista de vuelos
        "by_airline": rbt.new_map(),  # carrier -> lista de vuelos
        "by_distance": rbt.new_map()  # distancia -> lista de vuelos
    }
    return catalog


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def parse_time(hhmm):
    """Devuelve 'HH:MM' limpio o None si es inválido."""
    if not hhmm or ":" not in hhmm:
        return None
    hh, mm = hhmm.split(":")
    try:
        h, m = int(hh), int(mm)
        if 0 <= h < 24 and 0 <= m < 60:
            return f"{h:02d}:{m:02d}"
        return None
    except:
        return None

def calc_delay(real, sched):
    """Calcula retraso en minutos entre hora real y programada, corrigiendo medianoche."""
    if not real or not sched:
        return 0
    try:
        h1, m1 = map(int, real.split(":"))
        h2, m2 = map(int, sched.split(":"))
        total_real = h1 * 60 + m1
        total_sched = h2 * 60 + m2
        diff = total_real - total_sched

        # Corrige medianoche (si la diferencia es mayor a 12h o menor a -12h)
        if diff < -720:
            diff += 1440
        elif diff > 720:
            diff -= 1440

        return diff
    except:
        return 0

def calc_duration(dep, arr):
    """Duración en minutos sin datetime."""
    if not dep or not arr:
        return 0
    try:
        h1, m1 = map(int, dep.split(":"))
        h2, m2 = map(int, arr.split(":"))
        total1 = h1 * 60 + m1
        total2 = h2 * 60 + m2
        diff = total2 - total1
        if diff < 0:
            diff += 1440  # corrige medianoche
        return diff
    except:
        return 0

def add_to_index(index, key, flight):
    node = rbt.get(index, key)
    if node is None:
        lst = lt.new_list()
        lt.add_last(lst, flight)
        rbt.put(index, key, lst)
    else:
        lt.add_last(node, flight)


# ============================================================
# LIMPIEZA Y FORMATEO DEL VUELO
# ============================================================

def format_flight(raw):
    flight = {
        "id": raw["id"],
        "date": raw["date"],
        "dep_time": parse_time(raw["dep_time"]),
        "sched_dep_time": parse_time(raw["sched_dep_time"]),
        "arr_time": parse_time(raw["arr_time"]),
        "sched_arr_time": parse_time(raw["sched_arr_time"]),
        "carrier": raw["carrier"],
        "flight": raw["flight"],
        "tailnum": raw["tailnum"],
        "origin": raw["origin"],
        "dest": raw["dest"],
        "name": raw["name"]
    }

    # numéricos
    try:
        flight["air_time"] = float(raw["air_time"])
    except:
        flight["air_time"] = 0

    try:
        flight["distance"] = float(raw["distance"])
    except:
        flight["distance"] = 0

    # retrasos
    flight["dep_delay"] = calc_delay(flight["dep_time"], flight["sched_dep_time"])
    flight["arr_delay"] = calc_delay(flight["arr_time"], flight["sched_arr_time"])

    # duración
    flight["duration"] = (
        flight["air_time"]
        if flight["air_time"] > 0
        else calc_duration(flight["dep_time"], flight["arr_time"])
    )

    return flight



# ============================================================
# ORDENAMIENTO
# ============================================================

def sort_by_date_time(flights):
    """
    Ordena vuelos por fecha, luego por hora programada de salida,
    y finalmente por ID (para mantener el orden original del CSV).
    """
    def cmp(f1, f2):
        # comparar fecha
        if f1["date"] < f2["date"]:
            return True
        elif f1["date"] > f2["date"]:
            return False

        # misma fecha -> comparar hora programada
        t1, t2 = f1["sched_dep_time"], f2["sched_dep_time"]
        if not t1 and t2:
            return False
        if t1 and not t2:
            return True
        if t1 and t2 and t1 != t2:
            return t1 < t2

        # misma fecha y misma hora programada -> desempatar por id
        try:
            return int(f1["id"]) < int(f2["id"])
        except:
            return False

    return lt.merge_sort(flights, cmp)

# ============================================================
# CARGA DE DATOS (VERSIÓN SIMPLE Y ROBUSTA)
# ============================================================

def load_data(catalog, file_path):
    start = time.perf_counter()
    with codecs.open(file_path, "r", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            flight = format_flight(row)

            lt.add_last(catalog["flights"], flight)
            add_to_index(catalog["by_date"], flight["date"], flight)
            add_to_index(catalog["by_airline"], flight["carrier"], flight)
            add_to_index(catalog["by_distance"], flight["distance"], flight)

    flights_sorted = sort_by_date_time(catalog["flights"])
    total = lt.size(flights_sorted)

    first5 = lt.sub_list(flights_sorted, 0, min(5, total))
    last5 = lt.sub_list(flights_sorted, max(0, total - 5), min(5, total))

    end = time.perf_counter()

    return {
        "time": round((end - start) * 1000, 2),
        "total": total,
        "first5": first5,
        "last5": last5
    }


'''
# Funciones para la carga de datos

def load_data(catalog, flightsfile):
    start = get_time()

    with open(flightsfile, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            flight = format_flight(row)
            lt.add_last(mp.get(catalog, "vuelos")["value"], flight)
            add_to_indices(catalog, flight)

    end = get_time()

    # ordenar por fecha y hora programada
    sorted_flights = sort_flights_by_sched_datetime(mp.get(catalog, "vuelos")["value"])

    # preparar datos para el preview
    preview = []
    size = lt.size(sorted_flights)
    for i in range(1, 6):
        preview.append(get_flight_info(lt.get_element(sorted_flights, i)))
    for i in range(size - 4, size + 1):
        preview.append(get_flight_info(lt.get_element(sorted_flights, i)))

    return {
        "time_ms": delta_time(start, end),
        "total_flights": size,
        "preview": preview
    }

def sort_flights_by_sched_datetime(flights):
    """
    Ordena vuelos por fecha + hora programada de salida.
    """
    from datetime import datetime

    def key_func(f):
        try:
            date = f.get("date", "")
            sched = f.get("sched_dep_time", "")
            return datetime.strptime(f"{date} {sched}", "%Y-%m-%d %H:%M")
        except Exception:
            return datetime.max

    # Convertimos a lista Python, ordenamos y regresamos como array_list
    temp = [lt.get_element(flights, i) for i in range(0, lt.size(flights))]
    temp.sort(key=key_func)

    sorted_list = lt.new_list()
    for f in temp:
        lt.add_last(sorted_list, f)

    return sorted_list



# ==========================================================
# FORMATEO Y PREPROCESAMIENTO DE VUELOS
# ==========================================================



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

'''

def req_1(catalog, airline_code, min_delay, max_delay):
    start = get_time()

    # 1️⃣ Buscar lista de vuelos de esa aerolínea en el RBT
    flights = rbt.get(catalog["by_airline"], airline_code)
    if not flights:
        return {
            "time": 0,
            "total": 0,
            "filtered": lt.new_list()
        }

    # 2️⃣ Filtrar vuelos dentro del rango de retraso
    filtered = lt.new_list()
    size = lt.size(flights)
    for i in range(size):
        f = lt.get_element(flights, i)
        delay = f["dep_delay"]
        if delay is not None and min_delay <= delay <= max_delay:
            lt.add_last(filtered, f)

    # 3️⃣ Ordenar por retraso ascendente, luego fecha y hora
    def cmp(f1, f2):
        if f1["dep_delay"] != f2["dep_delay"]:
            return f1["dep_delay"] < f2["dep_delay"]
        elif f1["date"] != f2["date"]:
            return f1["date"] < f2["date"]
        return (f1["dep_time"] or "") < (f2["dep_time"] or "")

    sorted_filtered = lt.merge_sort(filtered, cmp)

    # 4️⃣ Calcular totales y tiempos
    total = lt.size(sorted_filtered)
    end = time.perf_counter()

    # 5️⃣ Sublistas de primeros y últimos 5
    first5 = lt.sub_list(sorted_filtered, 0, min(5, total))
    last5 = lt.sub_list(sorted_filtered, max(0, total - 5), min(5, total))

    return {
        "time": round((end - start) * 1000, 2),
        "total": total,
        "first5": first5,
        "last5": last5
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


def req_5(catalog, date_start, date_end, dest_code, top_n):
    """
    Retorna el resultado del requerimiento 5
    """

    start = get_time()

    flights_list = catalog["flights"]
    n_flights = lt.size(flights_list)

    
    airlines_map = mp.new_map(200, 0.5)

    
    i = 0
    while i < n_flights:
        flight = lt.get_element(flights_list, i)

        
        date = flight.get("date")
        dest = flight.get("dest")
        carrier = flight.get("carrier")

       
        process = True

        if not date or not dest or not carrier:
            process = False
        if process:
            if not (date_start <= date <= date_end):
                process = False
        if process:
            if dest != dest_code:
                process = False

        if process:
            delay = float(flight.get("arr_delay", 0))     
            duration = float(flight.get("duration", 0))
            distance = float(flight.get("distance", 0))

            record = mp.get(airlines_map, carrier)
            if record is None:
                record = {
                    "carrier": carrier,
                    "total_vuelos": 0,
                    "sum_delay": 0.0,
                    "sum_duration": 0.0,
                    "sum_distance": 0.0,
                    "max_dist_flight": None
                }
                mp.put(airlines_map, carrier, record)

            record["total_vuelos"] += 1
            record["sum_delay"] += delay
            record["sum_duration"] += duration
            record["sum_distance"] += distance

            
            max_f = record["max_dist_flight"]
            if max_f is None:
                record["max_dist_flight"] = flight
            else:
                current_max_dist = float(max_f.get("distance", 0))
                if distance > current_max_dist:
                    record["max_dist_flight"] = flight

        i += 1

   
    keys_struct = mp.key_set(airlines_map)

   
    if keys_struct is None or "elements" not in keys_struct:
        end = get_time()
        return {
            "time_ms": delta_time(start, end),
            "total_airlines": 0,
            "airlines": lt.new_list()
        }

    keys = keys_struct["elements"]
    if len(keys) == 0:
        end = get_time()
        return {
            "time_ms": delta_time(start, end),
            "total_airlines": 0,
            "airlines": lt.new_list()
        }

    pq_top = pq.new_heap(is_min_pq=True)

    idx = 0
    while idx < len(keys):
        carrier = keys[idx]
        record = mp.get(airlines_map, carrier)

        if record is not None:
            total = record["total_vuelos"]

            if total > 0:
                avg_delay = record["sum_delay"] / total
                avg_duration = record["sum_duration"] / total
                avg_distance = record["sum_distance"] / total

                record["avg_delay"] = avg_delay
                record["avg_duration"] = avg_duration
                record["avg_distance"] = avg_distance

                abs_punct = abs(avg_delay)
                record["abs_punctuality"] = abs_punct

                
                priority_key = (abs_punct, carrier)
                pq.insert(pq_top, priority_key, record)

        idx += 1

   
    result_list = lt.new_list()
    count = 0

    while not pq.is_empty(pq_top) and count < top_n:
        record = pq.remove(pq_top)
        lt.add_last(result_list, record)
        count += 1

    end = get_time()

    return {
        "time_ms": delta_time(start, end),
        "total_airlines": count,    
        "airlines": result_list      
    }

def req_6(catalog, date_start, date_end, min_distance, max_distance, top_m):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6

    start = get_time()

    flights_list = catalog["flights"]
    n_flights = lt.size(flights_list)

    min_distance = float(min_distance)
    max_distance = float(max_distance)

   
    airlines_map = mp.new_map(200, 0.5)

    
    i = 0
    while i < n_flights:
        flight = lt.get_element(flights_list, i)

        date = flight.get("date")
        carrier = flight.get("carrier")

        process = True

        if not date or not carrier:
            process = False

        if process:
            if not (date_start <= date <= date_end):
                process = False

        if process:
            distance = float(flight.get("distance", 0))
            if distance < min_distance or distance > max_distance:
                process = False

        if process:
            delay = float(flight.get("dep_delay", 0))

            record = mp.get(airlines_map, carrier)
            if record is None:
                record = {
                    "carrier": carrier,
                    "total_vuelos": 0,
                    "sum_delay": 0.0,
                    "sum_sq_delay": 0.0,
                    "mean_delay": 0.0,
                    "std_delay": 0.0,
                    "best_flight": None,
                    "best_diff": None
                }
                mp.put(airlines_map, carrier, record)

            record["total_vuelos"] += 1
            record["sum_delay"] += delay
            record["sum_sq_delay"] += delay * delay

        i += 1

    keys_struct = mp.key_set(airlines_map)

    if keys_struct is None or "elements" not in keys_struct:
        end = get_time()
        return {
            "time_ms": delta_time(start, end),
            "total_airlines": 0,
            "airlines": lt.new_list()
        }

    keys = keys_struct["elements"]
    if len(keys) == 0:
        end = get_time()
        return {
            "time_ms": delta_time(start, end),
            "total_airlines": 0,
            "airlines": lt.new_list()
        }

    
    idx = 0
    while idx < len(keys):
        carrier = keys[idx]
        record = mp.get(airlines_map, carrier)

        if record is not None:
            n = record["total_vuelos"]
            if n > 0:
                mean = record["sum_delay"] / n
                variance = (record["sum_sq_delay"] / n) - (mean * mean)
                if variance < 0:
                    variance = 0.0
                std = math.sqrt(variance)
            else:
                mean = 0.0
                std = 0.0

            record["mean_delay"] = mean
            record["std_delay"] = std
            record["best_flight"] = None
            record["best_diff"] = None

        idx += 1

  
    i = 0
    while i < n_flights:
        flight = lt.get_element(flights_list, i)

        date = flight.get("date")
        carrier = flight.get("carrier")

        process = True

        if not date or not carrier:
            process = False

        if process:
            if not (date_start <= date <= date_end):
                process = False

        if process:
            distance = float(flight.get("distance", 0))
            if distance < min_distance or distance > max_distance:
                process = False

        if process:
            record = mp.get(airlines_map, carrier)
            if record is not None:
                delay = float(flight.get("dep_delay", 0))
                diff = abs(delay - record["mean_delay"])

                if record["best_flight"] is None:
                    record["best_flight"] = flight
                    record["best_diff"] = diff
                else:
                    if diff < record["best_diff"]:
                        record["best_flight"] = flight
                        record["best_diff"] = diff

        i += 1

   
    pq_top = pq.new_heap(is_min_pq=True)

    idx = 0
    while idx < len(keys):
        carrier = keys[idx]
        record = mp.get(airlines_map, carrier)

        if record is not None:
            if record["total_vuelos"] > 0:
                priority_key = (record["std_delay"], record["mean_delay"])
                pq.insert(pq_top, priority_key, record)

        idx += 1

    
    result_list = lt.new_list()
    count = 0

    while (not pq.is_empty(pq_top)) and (count < top_m):
        record = pq.remove(pq_top)
        lt.add_last(result_list, record)
        count += 1

    end = get_time()

    return {
        "time_ms": delta_time(start, end),
        "total_airlines": count,
        "airlines": result_list
    }


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
