#!/bin/bash

# Nombre de la carpeta de destino
DESTINO="pdfs"

# Crear carpeta si no existe
mkdir -p "$DESTINO"

# Verificar si hay archivos .xopp
shopt -s nullglob
archivos=( *.xopp )

if [ ${#archivos[@]} -eq 0 ]; then
    echo " No hay archivos .xopp para convertir."
    exit 0
fi

# Recorrer archivos y convertir
for archivo in "${archivos[@]}"; do
    base="${archivo%.xopp}"
    salida="$DESTINO/$base.pdf"
    echo "Convirtiendo $archivo -> $salida ..."
    xournalpp --create-pdf="$salida" "$archivo"
done

echo "Conversión completa. Los PDF se guardaron en la carpeta '$DESTINO'."
