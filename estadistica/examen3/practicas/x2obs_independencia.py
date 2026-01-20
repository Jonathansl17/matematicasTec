filas = int(input("Cantidad de filas? "))
cols  = int(input("Cantidad de columnas? "))

OBSERVADOS = []
print("Ingrese la matriz observada:")
for i in range(filas):
    fila = []
    for j in range(cols):
        fila.append(int(input(f"OBSERVADOS[{i+1},{j+1}] = ")))
    OBSERVADOS.append(fila)


TX = [sum(OBSERVADOS[i]) for i in range(filas)]
TY = [sum(OBSERVADOS[i][j] for i in range(filas)) for j in range(cols)]
N  = sum(TX)


ESPERADOS = []
for i in range(filas):
    fila = []
    for j in range(cols):
        fila.append((TX[i] * TY[j]) / N)
    ESPERADOS.append(fila)


chi2_obs = 0
for i in range(filas):
    for j in range(cols):
        chi2_obs += (OBSERVADOS[i][j] - ESPERADOS[i][j])**2 / ESPERADOS[i][j]


print("\nTotales por fila (TX):", TX)
print("Totales por columna (TY):", TY)
print("Total N:", N)

print("\nMatriz de esperados (ESPERADOS):")
for fila in ESPERADOS:
    print([round(x, 4) for x in fila])

print("\nChi-cuadrado observado:")
print(round(chi2_obs, 6))
