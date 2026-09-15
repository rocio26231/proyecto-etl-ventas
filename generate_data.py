import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generar_datos_empresariales(num_registros=5000):
    print("Generando dataset empresarial masivo...")
    np.random.seed(42)
    random.seed(42)
    
    productos = {
        'Laptop Pro 15': 1200.00,
        'Monitor 4K': 350.00,
        'Teclado Mecánico': 80.00,
        'Mouse Inalámbrico': 30.00,
        'Auriculares Noise-Canceling': 150.00,
        'Silla Ergonómica': 250.00
    }
    
    clientes = [f"Cliente_{i}" for i in range(101, 600)]
    estados = ['Completado', 'Completado', 'Completado', 'Pendiente', 'Cancelado']
    
    data = []
    fecha_inicio = datetime(2026, 1, 1)
    
    for i in range(1, num_registros + 1):
        prod = random.choice(list(productos.keys()))
        precio = productos[prod]
        
        # Inyección de fallas reales de producción (nulos, negativos, formatos mixtos)
        if random.random() < 0.03:
            precio = np.nan
        
        cant = random.randint(-1, 5)
        cliente = f"  {random.choice(clientes)}  " if random.random() < 0.1 else random.choice(clientes)
        
        fecha = fecha_inicio + timedelta(days=random.randint(0, 250))
        fecha_str = fecha.strftime('%Y-%m-%d') if random.random() > 0.05 else fecha.strftime('%d/%m/%Y')
        
        data.append({
            'transaccion_id': 10000 + i,
            'fecha': fecha_str,
            'cliente': cliente,
            'producto': prod,
            'precio_unitario': precio,
            'cantidad': cant,
            'estado': random.choice(estados)
        })
    
    df = pd.DataFrame(data)
    
    # Inyectar un 4% de registros duplicados
    duplicados = df.sample(frac=0.04)
    df = pd.concat([df, duplicados], ignore_index=True)
    
    df.to_csv('datos_ventas_raw.csv', index=False)
    print(f"Dataset generado exitosamente con {len(df)} filas en 'datos_ventas_raw.csv'.")

if __name__ == "__main__":
    generar_datos_empresariales()