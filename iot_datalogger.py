"""
Simulador de ingesta y almacenamiento de telemetria IoT.
Guarda lecturas de temperatura y humedad en una base de datos SQLite local.
"""

import sqlite3
import random
import time
from datetime import datetime

# Archivo de la base de datos local
DB_NAME = "sensores_iot.db"


def inicializar_bd():
    """Crea la tabla de telemetria si no existe."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            dispositivo TEXT NOT NULL,
            temperatura REAL NOT NULL,
            humedad REAL NOT NULL,
            alerta INTEGER NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    print("Base de datos inicializada correctamente.")


def guardar_lectura(dispositivo, temperatura, humedad):
    """Registra una medicion en la base de datos."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Marcamos alerta si la temperatura supera los 28 grados
    alerta = 1 if temperatura > 28.0 else 0
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO telemetria (timestamp, dispositivo, temperatura, humedad, alerta)
        VALUES (?, ?, ?, ?, ?)
    """, (fecha_actual, dispositivo, temperatura, humedad, alerta))
    
    conn.commit()
    conn.close()
    
    estado = "[ALERTA TEMP]" if alerta == 1 else "[NORMAL]"
    print(f"[{fecha_actual}] {dispositivo} -> Temp: {temperatura:.1f} °C | Humedad: {humedad:.1f} % {estado}")


if __name__ == "__main__":
    inicializar_bd()
    sensor_id = "ESP32_SENSOR_01"
    
    print(f"\nIniciando muestreo para {sensor_id} (12 lecturas)...")
    print("-" * 55)
    
    for i in range(1, 13):
        # Rango de valores simulados para prueba
        temp = round(random.uniform(23.0, 31.5), 1)
        hum = round(random.uniform(45.0, 80.0), 1)
        
        guardar_lectura(sensor_id, temp, hum)
        time.sleep(1)
        
    print("-" * 55)
    print("Muestreo completado. Registros guardados en 'sensores_iot.db'.\n")
