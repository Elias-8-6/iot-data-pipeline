"""
Modulo de analisis y visualizacion de telemetria IoT.
Objetivo:
1. Extraer los datos desde la base de datos local SQLite hacia un DataFrame de Pandas.
2. Calcular metricas estadisticas descriptivas (promedios, maximos, minimos y alertas).
3. Visualizar el comportamiento temporal mediante subgraficas en Matplotlib.
"""

# sqlite3: Permite conectarse al archivo de la base de datos relacional local
import sqlite3

# pandas: Libreria para analisis de datos y manipulacion de tablas (DataFrames)
import pandas as pd

# matplotlib.pyplot: Libreria para generacion y renderizado de graficos
import matplotlib.pyplot as plt

# Nombre del archivo de base de datos generado por iot_datalogger.py
DB_NAME = "sensores_iot.db"


def procesar_datos():
    """
    Funcion principal que coordina la extraccion, calculo de metricas
    y generacion del panel grafico de monitoreo.
    """
    
    # -------------------------------------------------------------------------
    # 1. EXTRACCION DE DATOS DESDE SQLITE A PANDAS
    # -------------------------------------------------------------------------
    # Abrimos la conexion hacia el archivo local .db
    conn = sqlite3.connect(DB_NAME)
    
    # Consulta SQL para seleccionar solo las columnas requeridas para el analisis
    query = "SELECT timestamp, temperatura, humedad, alerta FROM telemetria"
    
    # pd.read_sql_query ejecuta la consulta y convierte el resultado directamente
    # en un DataFrame de Pandas. Esto asigna automaticamente los nombres de las
    # columnas y detecta los tipos de datos sin necesidad de hacer bucles manuales.
    df = pd.read_sql_query(query, conn)
    
    # Cerramos la conexion de la base de datos para liberar memoria y recursos
    conn.close()
    
    # Validacion defensiva: verificar si la tabla tiene datos antes de procesar
    if df.empty:
        print("La base de datos no contiene registros. Ejecute 'iot_datalogger.py' primero.")
        return

    # -------------------------------------------------------------------------
    # 2. TRANSFORMACION DE TIPOS Y SERIES DE TIEMPO
    # -------------------------------------------------------------------------
    # La columna 'timestamp' se almacena como texto (string) en SQLite.
    # pd.to_datetime la convierte al tipo datetime64, lo que permite ordenar,
    # filtrar cronologicamente y formatear correctamente los ejes temporales.
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # -------------------------------------------------------------------------
    # 3. ANALISIS ESTADISTICO VECTORIZADO CON PANDAS
    # -------------------------------------------------------------------------
    # Pandas procesa columnas enteras de forma vectorizada (escritas en C/NumPy),
    # siendo mucho mas rapido que recorrer una lista con un ciclo 'for'.
    promedio_temp = df['temperatura'].mean()   # Media aritmetica de temperatura
    max_temp = df['temperatura'].max()         # Valor maximo registrado de temperatura
    min_temp = df['temperatura'].min()         # Valor minimo registrado de temperatura
    promedio_hum = df['humedad'].mean()        # Media aritmetica de humedad relativa
    total_alertas = df['alerta'].sum()         # Suma de la columna binaria (1=alerta, 0=normal)
    
    # Presentacion de metricas calculadas en la consola
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

    # -------------------------------------------------------------------------
    # 4. CONFIGURACION DEL DASHBOARD GRAFICO CON MATPLOTLIB
    # -------------------------------------------------------------------------
    # plt.subplots crea la ventana general (fig) y dos paneles (ax1 y ax2):
    # - nrows=2, ncols=1 : 2 filas de graficos alineadas verticalmente
    # - figsize=(9, 6)   : Ancho y alto de la figura en pulgadas
    # - sharex=True      : Sincroniza el eje X (tiempo) entre ambas graficas
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(9, 6), sharex=True)
    fig.suptitle("Monitoreo IoT en Tiempo Real (Nodo Invernadero)", fontsize=13, fontweight="bold")
    
    # --- PANEL SUPERIOR: TEMPERATURA (ax1) ---
    # Dibujamos la serie temporal con linea roja continua y puntos en cada medicion
    ax1.plot(df['timestamp'], df['temperatura'], color='crimson', marker='o', linewidth=2, label='Temperatura (°C)')
    
    # axhline dibuja una linea horizontal punteada que marca el limite critico (28°C)
    ax1.axhline(y=28.0, color='darkred', linestyle='--', linewidth=1.5, label='Umbral alerta (28°C)')
    ax1.set_ylabel("Temp (°C)")
    ax1.legend(loc='upper right')           # Muestra el cuadro explicativo de las series
    ax1.grid(True, linestyle=':', alpha=0.6) # Rejilla punteada para facilitar la lectura visual
    
    # --- PANEL INFERIOR: HUMEDAD (ax2) ---
    # Dibujamos la serie de humedad con linea azul y marcadores cuadrados
    ax2.plot(df['timestamp'], df['humedad'], color='royalblue', marker='s', linewidth=2, label='Humedad (%)')
    ax2.set_ylabel("Humedad (%)")
    ax2.set_xlabel("Hora")                  # Etiqueta del eje horizontal solo en la grafica inferior
    ax2.legend(loc='upper right')
    ax2.grid(True, linestyle=':', alpha=0.6)
    
    # autofmt_xdate inclina y ajusta las marcas de fecha/hora para que no choquen
    fig.autofmt_xdate()
    
    # tight_layout ajusta los margenes para que no se corten etiquetas ni titulos
    plt.tight_layout()
    
    # -------------------------------------------------------------------------
    # 5. EXPORTACION Y RENDERIZADO INTERACTIVO
    # -------------------------------------------------------------------------
    # Guardamos la grafica como imagen PNG en alta resolucion (200 dpi) para reportes
    archivo_grafica = "grafica_sensores_iot.png"
    plt.savefig(archivo_grafica, dpi=200)
    print(f"Grafica guardada exitosamente en '{archivo_grafica}'.")
    print("Mostrando ventana grafica (cierre la ventana para terminar la ejecucion)...")
    
    # plt.show abre la interfaz grafica interactiva en pantalla.
    # El bloque try/except previene que se muestre un error feo en terminal si se interrumpe con Ctrl+C.
    try:
        plt.show()
    except KeyboardInterrupt:
        pass


# Punto de entrada estandar cuando el script se ejecuta directamente
if __name__ == "__main__":
    procesar_datos()
