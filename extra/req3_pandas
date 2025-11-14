import pandas as pd
import numpy as np
import datetime
import time
import os
from tabulate import tabulate

# ============================================================
# PARSER ROBUSTO DE HORAS (acepta errores tipo "11:5")
# ============================================================
def parse_hhmm(t):
    if pd.isna(t):
        return None
    t = str(t).strip()

    if ":" not in t:  
        # Caso "11" o "5"
        try:
            h = int(t)
            return datetime.time(h, 0)
        except:
            return None

    hh, mm = t.split(":")[:2]
    try:
        h = int(hh)
        m = int(mm)
        if 0 <= h < 24 and 0 <= m < 60:
            return datetime.time(h, m)
    except:
        return None
    return None


# ============================================================
# VALIDATOR STANDALONE + TABLA
# ============================================================
def req4_pandas_standalone(date_start, date_end, time_start, time_end, top_n):

    print("\n=== VALIDACIÓN REQ 4 (PANDAS) ===")

    start = time.perf_counter()

    # === RUTA ===
    data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'
    file_path = data_dir + "flights_large.csv"

    # === LEER CSV ===
    df = pd.read_csv(file_path)

    # === PARSEAR FECHAS ===
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

    # === PARSEAR HORAS ===
    df["sched_dep_time"] = df["sched_dep_time"].apply(parse_hhmm)
    df["dep_time"] = df["dep_time"].apply(parse_hhmm)
    df["arr_time"] = df["arr_time"].apply(parse_hhmm)

    # ============================================================
    # DURACIÓN: usar air_time o cálculo manual
    # ============================================================
    def compute_duration(r):
        if not np.isnan(r["air_time"]):
            return r["air_time"]

        t1 = r["dep_time"]
        t2 = r["arr_time"]
        if t1 is None or t2 is None:
            return 0

        m1 = t1.hour * 60 + t1.minute
        m2 = t2.hour * 60 + t2.minute

        diff = m2 - m1
        if diff < 0:
            diff += 1440
        return diff

    df["duration"] = df.apply(compute_duration, axis=1)

    # ============================================================
    # FILTROS
    # ============================================================
    d_start = pd.to_datetime(date_start)
    d_end = pd.to_datetime(date_end)

    t_start = parse_hhmm(time_start)
    t_end = parse_hhmm(time_end)

    df = df[
        (df["date"] >= d_start) &
        (df["date"] <= d_end) &
        (df["sched_dep_time"] >= t_start) &
        (df["sched_dep_time"] <= t_end)
    ]

    if df.empty:
        print("\nNo hay vuelos que cumplan el filtro.")
        return

    # ============================================================
    # AGRUPAR POR AEROLÍNEA
    # ============================================================
    groups = df.groupby("carrier")

    rows = []

    for carrier, g in groups:
        total = len(g)
        prom_dur = g["duration"].mean()
        prom_dist = g["distance"].mean()

        # Vuelo mínimo
        g_sorted = g.sort_values(
            by=["duration", "date", "sched_dep_time"],
            ascending=[True, True, True]
        )
        mf = g_sorted.iloc[0]

        rows.append({
            "carrier": carrier,
            "total_vuelos": int(total),
            "prom_duracion": float(prom_dur),
            "prom_distancia": float(prom_dist),
            "min_flight": {
                "id": int(mf["id"]),
                "flight": int(mf["flight"]),
                "date": mf["date"].strftime("%Y-%m-%d"),
                "sched_dep_time": mf["sched_dep_time"].strftime("%H:%M") if mf["sched_dep_time"] else "Unknown",
                "origin": mf["origin"],
                "dest": mf["dest"],
                "duration": float(mf["duration"])
            }
        })

    # ============================================================
    # ORDENAR POR TOTAL_VUELOS (desc) + carrier asc
    # ============================================================
    rows.sort(key=lambda r: (-r["total_vuelos"], r["carrier"]))

    rows = rows[:top_n]

    end = time.perf_counter()

    # ============================================================
    # IMPRIMIR TABLA EXACTA A TU VIEW
    # ============================================================
    print(f"\nTiempo de ejecución: {round((end - start) * 1000, 3)} ms")
    print(f"Aerolíneas consideradas: {len(rows)}\n")

    headers = [
        "Código",
        "Total Vuelos",
        "Prom. Duración",
        "Prom. Distancia",
        "ID Mínimo",
        "Código Vuelo",
        "Fecha",
        "Hora Programada",
        "Origen",
        "Destino",
        "Duración"
    ]

    table = []

    for rec in rows:
        mf = rec["min_flight"]
        row = [
            rec["carrier"],
            rec["total_vuelos"],
            round(rec["prom_duracion"], 2),
            round(rec["prom_distancia"], 2),
            mf["id"],
            mf["flight"],
            mf["date"],
            mf["sched_dep_time"],
            mf["origin"],
            mf["dest"],
            mf["duration"]
        ]
        table.append(row)

    print(tabulate(table, headers=headers, tablefmt="grid"))

req4_pandas_standalone(
    "2013-01-01",
    "2013-06-01",
    "11:55",
    "23:23",
    4
)
