import pandas as pd
import datetime
import time
import os

data_dir = os.path.dirname(os.path.realpath('__file__')) + '/Data/'
file_path = data_dir + "flights_large.csv"

def verify_req1_with_pandas(file_path, airline_code, min_delay, max_delay):
    start = time.perf_counter()

    # ============================================================
    # 1. Leer CSV
    # ============================================================
    df = pd.read_csv(file_path)

    # ============================================================
    # 2. Conversión de tiempos
    # ============================================================
    def to_time(x):
        try:
            if pd.isna(x) or ":" not in str(x):
                return None
            h, m = map(int, str(x).split(":"))
            return datetime.time(h, m)
        except:
            return None

    for col in ["dep_time", "sched_dep_time"]:
        df[col] = df[col].apply(to_time)

    # ============================================================
    # 3. Calcular retraso de salida (idéntico a tu lógica)
    # ============================================================
    def calc_delay(real, sched):
        if pd.isna(real) or pd.isna(sched) or real is None or sched is None:
            return 0
        h1, m1 = real.hour, real.minute
        h2, m2 = sched.hour, sched.minute
        total_real = h1 * 60 + m1
        total_sched = h2 * 60 + m2
        diff = total_real - total_sched
        # Corrige medianoche (cruce de día)
        if diff < -720:
            diff += 1440
        elif diff > 720:
            diff -= 1440
        return diff

    df["dep_delay"] = df.apply(lambda r: calc_delay(r["dep_time"], r["sched_dep_time"]), axis=1)

    # ============================================================
    # 4. Filtro por aerolínea y rango de retraso
    # ============================================================
    mask = (df["carrier"] == airline_code) & (df["dep_delay"] >= min_delay) & (df["dep_delay"] <= max_delay)
    df_filtered = df[mask].copy()

    # ============================================================
    # 5. Ordenamiento según especificaciones
    # ============================================================
    df_filtered["date"] = pd.to_datetime(df_filtered["date"], errors="coerce")
    df_filtered = df_filtered.sort_values(by=["dep_delay", "date", "dep_time"], ascending=[True, True, True])

    total = len(df_filtered)
    first5 = df_filtered.head(5)
    last5 = df_filtered.tail(5)

    end = time.perf_counter()

    print(f"\n=== VERIFICACIÓN REQ 1 CON PANDAS ===")
    print(f"Aerolínea: {airline_code} | Rango retraso: [{min_delay}, {max_delay}] minutos")
    print(f"Tiempo total de ejecución: {round((end - start) * 1000, 2)} ms")
    print(f"Total de vuelos filtrados: {total}")

    # ============================================================
    # 6. Mostrar primeros y últimos 5 vuelos
    # ============================================================
    cols = ["id", "flight", "date", "name", "carrier", "origin", "dest", "dep_delay"]

    print("\nPrimeros 5 vuelos:")
    print(first5[cols])

    print("\nÚltimos 5 vuelos:")
    print(last5[cols])


# ============================================================
# Ejemplo de ejecución (usa los mismos parámetros que tu req1)
# ============================================================
verify_req1_with_pandas(file_path, airline_code="UA", min_delay=10, max_delay=30)
