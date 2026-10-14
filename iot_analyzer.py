"""
Modulo de analisis y graficacion de datos de sensores IoT.
Lee los registros desde SQLite, calcula metricas con Pandas y genera graficos con Matplotlib.
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_NAME = "sensores_iot.db"


def procesar_datos():
    # Leer datos guardados en SQLite
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT timestamp, temperatura, humedad, alerta FROM telemetria"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if df.empty:
        print("La base de datos no contiene registros. Ejecute 'iot_datalogger.py' primero.")
        return

    # Convertir a formato datetime para manejo de series temporales
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Calculo de metricas descriptivas
    promedio_temp = df['temperatura'].mean()
    max_temp = df['temperatura'].max()
    min_temp = df['temperatura'].min()
    promedio_hum = df['humedad'].mean()
    total_alertas = df['alerta'].sum()
    
    print("\n" + "=" * 45)
    print("      REPORTE DE DATOS TELEMETRICOS IOT      ")
    print("=" * 45)
    print(f"Total de registros analizados : {len(df)}")
    print(f"Temperatura promedio          : {promedio_temp:.2f} °C")
    print(f"Temperatura maxima            : {max_temp:.2f} °C")
    print(f"Temperatura minima            : {min_temp:.2f} °C")
    print(f"Humedad promedio              : {promedio_hum:.2f} %")
    print(f"Lecturas con alerta (T > 28°C): {total_alertas}")
    print("=" * 45 + "\n")

    # Generacion de graficas (temperatura y humedad)
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(9, 6), sharex=True)
    fig.suptitle("Monitoreo IoT en Tiempo Real (Nodo Invernadero)", fontsize=13, fontweight="bold")
    
    # Grafica de temperatura
    ax1.plot(df['timestamp'], df['temperatura'], color='crimson', marker='o', linewidth=2, label='Temperatura (°C)')
    ax1.axhline(y=28.0, color='darkred', linestyle='--', linewidth=1.5, label='Umbral alerta (28°C)')
    ax1.set_ylabel("Temp (°C)")
    ax1.legend(loc='upper right')
    ax1.grid(True, linestyle=':', alpha=0.6)
    
    # Grafica de humedad
    ax2.plot(df['timestamp'], df['humedad'], color='royalblue', marker='s', linewidth=2, label='Humedad (%)')
    ax2.set_ylabel("Humedad (%)")
    ax2.set_xlabel("Hora")
    ax2.legend(loc='upper right')
    ax2.grid(True, linestyle=':', alpha=0.6)
    
    fig.autofmt_xdate()
    plt.tight_layout()
    
    # Guardar grafica generada
    archivo_grafica = "grafica_sensores_iot.png"
    plt.savefig(archivo_grafica, dpi=200)
    print(f"Grafica guardada exitosamente en '{archivo_grafica}'.")
    print("Mostrando ventana grafica (cierre la ventana para terminar la ejecucion)...")
    
    try:
        plt.show()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    procesar_datos()
