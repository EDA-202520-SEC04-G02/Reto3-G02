import pandas as pd
import datetime
import time
import os

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'
file_path = data_dir + "flights_large.csv"

def verify_with_pandas(file_path):
    start = time.perf_counter()

    # Leer CSV
    df = pd.read_csv(file_path)

    # ============================================================
    # Conversiones de tiempo
    # ============================================================
    def to_time(x):
        try:
            if pd.isna(x) or ":" not in str(x):
                return None
            h, m = map(int, str(x).split(":"))
            return datetime.time(h, m)
        except:
            return None

    df["dep_time"] = df["dep_time"].apply(to_time)
    df["sched_dep_time"] = df["sched_dep_time"].apply(to_time)
    df["arr_time"] = df["arr_time"].apply(to_time)
    df["sched_arr_time"] = df["sched_arr_time"].apply(to_time)

    # ============================================================
    # Función auxiliar para calcular retrasos (igual que tu lógica)
    # ============================================================
    def calc_delay(real, sched):
        if pd.isna(real) or pd.isna(sched) or real is None or sched is None:
            return 0
        h1, m1 = real.hour, real.minute
        h2, m2 = sched.hour, sched.minute
        total_real = h1 * 60 + m1
        total_sched = h2 * 60 + m2
        diff = total_real - total_sched
        if diff < -720:
            diff += 1440
        elif diff > 720:
            diff -= 1440
        return diff

    # ============================================================
    # Calcular retrasos
    # ============================================================
    df["dep_delay"] = df.apply(lambda r: calc_delay(r["dep_time"], r["sched_dep_time"]), axis=1)
    df["arr_delay"] = df.apply(lambda r: calc_delay(r["arr_time"], r["sched_arr_time"]), axis=1)


    # ============================================================
    # Ordenar según guía oficial
    # ============================================================
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df_sorted = df.sort_values(by=["date", "sched_dep_time", "id"], ascending=[True, True, True])

    first5 = df_sorted.head(5)
    last5 = df_sorted.tail(5)

    end = time.perf_counter()

    print(f"\n=== VERIFICACIÓN CON PANDAS ===")
    print(f"Tiempo de carga y ordenamiento: {round((end - start) * 1000, 2)} ms")
    print(f"Total de vuelos cargados: {len(df)}")

    def fmt_time(t):
        if isinstance(t, datetime.time):
            return t.strftime("%H:%M")
        return "Unknown"

    # ============================================================
    # Mostrar resultados
    # ============================================================
    cols = [
        "date", "dep_time", "arr_time", "sched_dep_time", "sched_arr_time",
        "carrier", "name", "tailnum", "origin", "dest",
        "air_time", "distance", "dep_delay", "arr_delay"
    ]

    print("\nPrimeros 5 vuelos:")
    print(first5[cols])

    print("\nÚltimos 5 vuelos:")
    print(last5[cols])

# Ejecutar
verify_with_pandas(file_path)
