# ==========================================
# 1. PRÁCTICA DE TUPLAS
# ==========================================
# Las tuplas son inmutables. Accedemos con índices []
A = ("Data", (10, 20, 30))

# Para sacar el 20: entramos al índice 1 (la tupla interna) y luego al índice 1
valor_20 = A[1][1]
print("1. Tuplas - Resultado:", valor_20)


# ==========================================
# 2. PRÁCTICA DE LISTAS
# ==========================================
# Las listas son mutables. Usamos .append() para agregar elementos
lista = [1, 2]
lista.append(3)
print("2. Listas - Resultado:", lista)

# Para clonar una lista de forma independiente usas [:]
copia_lista = lista[:]


# ==========================================
# 3. PRÁCTICA DE DICCIONARIOS
# ==========================================
# Estructura clave: valor. Usamos .keys() para obtener las claves
d = {"usuario": "admin", "pass": 1234}
mis_claves = d.keys()
print("3. Diccionarios - Resultado:", mis_claves)


# ==========================================
# 4. PRÁCTICA DE CONJUNTOS (SETS)
# ==========================================
# Colección de elementos únicos sin duplicados
conjunto = {10, 20, 30}
print("4. Conjuntos - ¿Existe el 20?:", 20 in conjunto)