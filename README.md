Enterprise E-Commerce Data Pipeline & Analytics Engine

## 📌 Descripción
Pipeline ETL modular de nivel empresarial para procesar datos de e-commerce con anomalías típicas de producción (duplicados, valores nulos, formatos de fecha mixtos y errores de stock). Los datos procesados se modelan en un Data Warehouse en SQLite.

## 🛠️ Tecnologías
* Python 3.x (Pandas, NumPy)
* SQLite3 (Data Warehouse Relacional)
* Python Logging (Auditoría)
* SQL Avanzado (CTEs, Window Functions `DENSE_RANK`)

## 📁 Estructura del Proyecto
* `generate_data.py`: Generador de dataset masivo con anomalías.
* `etl_pipeline.py`: Pipeline ETL con logging e imputación lógica.
* `queries.sql`: Consultas SQL para analítica de negocio.
* `pipeline_execution.log`: Registro de auditoría del proceso.
* `empresa_dw.db`: Data Warehouse en SQLite.

## 🚀 Ejecución
```bash
pip install pandas numpy
python generate_data.py
python etl_pipeline.py