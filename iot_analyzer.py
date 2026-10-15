import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_NAME = "sensores_iot.db"


def procesar_datos():
    # Conectar a la base de datos y leer la tabla
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT timestamp, temperatura, humedad, alerta FROM telemetria"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Validar si hay datos guardados
    if df.empty:
        print("La base de datos esta vacia. Corre primero iot_datalogger.py")
        return

    # Convertir fecha a datetime para ordenar y graficar bien
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Calculo de metricas con pandas
    promedio_temp = df['temperatura'].mean()
    max_temp = df['temperatura'].max()
    min_temp = df['temperatura'].min()
    promedio_hum = df['humedad'].mean()
    total_alertas = df['alerta'].sum()
    
    # Imprimir reporte en consola
    print("\nREPORTE DE DATOS IOT")
    print("-" * 35)
    print(f"Total registros: {len(df)}")
    print(f"Temp promedio: {promedio_temp:.2f} °C")
    print(f"Temp maxima: {max_temp:.2f} °C")
    print(f"Temp minima: {min_temp:.2f} °C")
    print(f"Humedad promedio: {promedio_hum:.2f} %")
    print(f"Alertas (>28°C): {total_alertas}")
    print("-" * 35 + "\n")

    # Crear la figura con dos graficas verticales que comparten eje x
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(9, 6), sharex=True)
    fig.suptitle("Monitoreo IoT en Tiempo Real", fontsize=13, fontweight="bold")
    
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
    
    # Formato de fechas y margenes
    fig.autofmt_xdate()
    plt.tight_layout()
    
    # Guardar imagen y abrir ventana grafica
    archivo_grafica = "grafica_sensores_iot.png"
    plt.savefig(archivo_grafica, dpi=200)
    print(f"Grafica guardada en '{archivo_grafica}'")
    print("Mostrando ventana grafica (cerrar ventana para finalizar)...")
    
    try:
        plt.show()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    procesar_datos()
