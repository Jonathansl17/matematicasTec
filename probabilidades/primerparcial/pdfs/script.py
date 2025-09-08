import os

# Obtener el directorio actual
carpeta = os.getcwd()

for nombre in os.listdir(carpeta):
    ruta_antigua = os.path.join(carpeta, nombre)

    # Evitar directorios
    if os.path.isfile(ruta_antigua):
        nuevo_nombre = nombre.lower()
        ruta_nueva = os.path.join(carpeta, nuevo_nombre)

        # Solo renombrar si cambia
        if ruta_antigua != ruta_nueva:
            print(f"Renombrando: {nombre} -> {nuevo_nombre}")
            os.rename(ruta_antigua, ruta_nueva)

print("✅ Renombrado completado")
