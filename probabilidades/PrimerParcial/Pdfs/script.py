import os

# Iterar sobre los archivos en el directorio actual
for filename in os.listdir('.'):
    if ' ' in filename:  # Si el nombre contiene espacios
        new_name = filename.replace(' ', '_')
        os.rename(filename, new_name)
        print(f"Renombrado: {filename} -> {new_name}")

print("Renombrado completado.")
