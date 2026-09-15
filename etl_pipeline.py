import pandas as pd
import sqlite3
import logging
import sys

# ---------------------------------------------------------
# CONFIGURACIÓN DE LOGGING (Auditoría de Producción)
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("pipeline_execution.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def ejecutar_etl_pipeline():
    logging.info("=== INICIANDO PIPELINE ETL EMPRESARIAL ===")
    
    # ---------------------------------------------------------
    # 1. EXTRACCIÓN (EXTRACT)
    # ---------------------------------------------------------
    archivo_origen = 'datos_ventas_raw.csv'
    try:
        df_raw = pd.read_csv(archivo_origen)
        logging.info(f"Extracción exitosa: {len(df_raw)} registros leídos de '{archivo_origen}'.")
    except Exception as e:
        logging.error(f"Error crítico en la extracción: {e}")
        return

    # ---------------------------------------------------------
    # 2. TRANSFORMACIÓN (TRANSFORM)
    # ---------------------------------------------------------
    logging.info("Iniciando fase de limpieza y transformación de datos...")
    
    # a. Eliminación de Duplicados
    filas_iniciales = len(df_raw)
    df_clean = df_raw.drop_duplicates()
    duplicados_removidos = filas_iniciales - len(df_clean)
    logging.info(f"Duplicados eliminados: {duplicados_removidos} filas.")

    # b. Normalización de Nombres de Clientes y Productos
    df_clean['cliente'] = df_clean['cliente'].astype(str).str.strip().str.title()
    df_clean['producto'] = df_clean['producto'].astype(str).str.strip().str.title()

    # c. Normalización de Fechas (Formatos mixtos a YYYY-MM-DD)
    df_clean['fecha'] = pd.to_datetime(df_clean['fecha'], format='mixed').dt.strftime('%Y-%m-%d')

    # d. Imputación de Precios Faltantes según el Catálogo de Productos
    precios_catalogo = {
        'Laptop Pro 15': 1200.00,
        'Monitor 4K': 350.00,
        'Teclado Mecánico': 80.00,
        'Mouse Inalámbrico': 30.00,
        'Auriculares Noise-Canceling': 150.00,
        'Silla Ergonómica': 250.00
    }
    
    nulos_precio_antes = df_clean['precio_unitario'].isna().sum()
    df_clean['precio_unitario'] = df_clean['precio_unitario'].fillna(
        df_clean['producto'].map(precios_catalogo)
    )
    logging.info(f"Precios nulos imputados: {nulos_precio_antes} registros.")

    # e. Filtrado de Incoherencias de Stock (Cantidades <= 0)
    invalidos_cant = len(df_clean[df_clean['cantidad'] <= 0])
    df_clean = df_clean[df_clean['cantidad'] > 0]
    logging.info(f"Registros descartados por cantidad inválida (<= 0): {invalidos_cant}.")

    # f. Creación de Métricas de Negocio
    df_clean['monto_total'] = df_clean['precio_unitario'] * df_clean['cantidad']
    logging.info(f"Transformación completada. Registros limpios finales: {len(df_clean)}.")

    # ---------------------------------------------------------
    # 3. CARGA (LOAD) Y MODELADO SQL
    # ---------------------------------------------------------
    base_datos = 'empresa_dw.db'
    logging.info(f"Conectando al Data Warehouse SQLite '{base_datos}'...")
    
    try:
        conn = sqlite3.connect(base_datos)
        
        # Carga de la Tabla de Hechos (Fact Table)
        df_clean.to_sql('fact_ventas', conn, if_exists='replace', index=False)
        logging.info("Tabla de hechos 'fact_ventas' cargada correctamente.")
        
        # Carga de Tabla Dimensión Productos
        df_productos = df_clean[['producto', 'precio_unitario']].drop_duplicates()
        df_productos.to_sql('dim_productos', conn, if_exists='replace', index=False)
        logging.info("Tabla dimensión 'dim_productos' cargada correctamente.")
        
        conn.close()
        logging.info("=== PIPELINE EJECUTADO Y AUDITADO CON ÉXITO ===")
        
    except Exception as e:
        logging.error(f"Error durante la carga en la Base de Datos: {e}")

if __name__ == "__main__":
    ejecutar_etl_pipeline()