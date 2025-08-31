import os

# Iterar sobre los archivos en el directorio actual
for filename in os.listdir('.'):
    # Si el archivo tiene espacios en el nombre
    if ' ' in filename:
        new_name = filename.replace(' ', '_')
        os.rename(filename, new_name)
        print(f'Renombrado: {filename} -> {new_name}')

print("Renombrado completado.")
