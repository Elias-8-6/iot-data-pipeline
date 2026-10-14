# Proyecto de Telemetría IoT: Ingesta, Persistencia y Análisis de Datos

**Asignatura:** Desarrollo de Software VIII  
**Institución:** Universidad Tecnológica de Panamá — Centro Regional de Chiriquí  

## Descripción
Este proyecto implementa un pipeline sencillo para la gestión de datos generados por un nodo sensor IoT (simulado):
1. **Ingesta y Persistencia:** Registro de lecturas periódicas de temperatura y humedad en una base de datos local utilizando `sqlite3`.
2. **Procesamiento de Datos:** Consulta y cálculo de métricas estadísticas básicas (promedios, máximos, mínimos y alertas) mediante `pandas`.
3. **Visualización:** Generación de gráficas de series de tiempo con umbrales de alerta utilizando `matplotlib`.

## Requisitos
- Python 3.8 o superior
- Dependencias indicadas en `requirements.txt`:
  ```bash
  pip install -r requirements.txt
  ```

## Estructura de Archivos
- `iot_datalogger.py`: Script que simula las lecturas del dispositivo sensor y las inserta en la base de datos `sensores_iot.db`.
- `iot_analyzer.py`: Script que lee la base de datos, imprime el resumen estadístico por consola y genera la gráfica comparativa.
- `requirements.txt`: Archivo de dependencias del proyecto.

## Uso

1. Ejecutar el recolector de datos para crear la base de datos y generar las muestras de prueba:
   ```bash
   python iot_datalogger.py
   ```

2. Ejecutar el analizador para ver el reporte en consola y visualizar las gráficas:
   ```bash
   python iot_analyzer.py
   ```
