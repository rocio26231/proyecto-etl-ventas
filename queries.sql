-- =========================================================
-- PROYECTO ETL VENTAS: CAPA DE ANALÍTICA Y BUSINESS INTELLIGENCE
-- =========================================================

-- 1. Métrica General: Total de Facturación y Ventas por Estado
SELECT 
    estado,
    COUNT(transaccion_id) AS total_transacciones,
    SUM(monto_total) AS facturacion_total,
    ROUND(AVG(monto_total), 2) AS ticket_promedio
FROM fact_ventas
GROUP BY estado
ORDER BY facturacion_total DESC;


-- 2. Ranking de Productos Más Vendidos (Uso de Window Functions - DENSE_RANK)
WITH resumen_productos AS (
    SELECT 
        producto,
        SUM(cantidad) AS unidades_vendidas,
        SUM(monto_total) AS ingreso_total
    FROM fact_ventas
    WHERE estado = 'Completado'
    GROUP BY producto
)
SELECT 
    producto,
    unidades_vendidas,
    ingreso_total,
    DENSE_RANK() OVER (ORDER BY ingreso_total DESC) AS ranking_ingresos
FROM resumen_productos;


-- 3. Top 10 Clientes VIP por Facturación
SELECT 
    cliente,
    COUNT(transaccion_id) AS total_compras,
    SUM(monto_total) AS total_gastado
FROM fact_ventas
WHERE estado = 'Completado'
GROUP BY cliente
ORDER BY total_gastado DESC
LIMIT 10;


-- 4. Tendencia Mensual de Ventas (Agrupación por Mes/Año)
SELECT 
    strftime('%Y-%m', fecha) AS mes,
    COUNT(transaccion_id) AS transacciones_completadas,
    SUM(monto_total) AS ingresos_mensuales
FROM fact_ventas
WHERE estado = 'Completado'
GROUP BY mes
ORDER BY mes ASC;