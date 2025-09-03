#!/usr/bin/env python3
import os
import re
import sys
import argparse

SPACE_RE = re.compile(r"\s+")

def es_puramente_numerica(nombre: str) -> bool:
    return nombre.isdigit()

def transformar_nombre(nombre: str) -> str:
    # minusculas + espacios y espacios múltiples a "_"
    snake = SPACE_RE.sub("_", nombre.strip().lower())
    return snake

def renombrar_directorios(path=".", recursivo=False, dry_run=False):
    try:
        with os.scandir(path) as it:
            for entry in it:
                # Solo directorios reales (ignorar enlaces simbólicos)
                if not entry.is_dir(follow_symlinks=False):
                    continue

                original = entry.name

                # Dejar intactos los nombres puramente numéricos
                if es_puramente_numerica(original):
                    print(f"Saltando (numérica): {original}")
                    # Si es recursivo, entrar igual al subdir numérico sin renombrarlo
                    if recursivo:
                        renombrar_directorios(os.path.join(path, original), recursivo, dry_run)
                    continue

                destino_nombre = transformar_nombre(original)
                origen = os.path.join(path, original)
                destino = os.path.join(path, destino_nombre)

                # Si no hay cambios de nombre, solo continuar (pero seguir recursión si aplica)
                if destino_nombre == original:
                    if recursivo:
                        renombrar_directorios(origen, recursivo, dry_run)
                    continue

                # Evitar conflicto si ya existe el destino
                if os.path.exists(destino) and os.path.realpath(origen) != os.path.realpath(destino):
                    print(f"⚠️  Ya existe '{destino_nombre}'. No renombro '{original}'.")
                    # Aun así, si es recursivo, entrar al origen
                    if recursivo:
                        renombrar_directorios(origen, recursivo, dry_run)
                    continue

                if dry_run:
                    print(f"[DRY-RUN] {original}  →  {destino_nombre}")
                    # Recursivo: entrar al nombre ORIGINAL (aún no se renombra)
                    if recursivo:
                        renombrar_directorios(origen, recursivo, dry_run)
                else:
                    try:
                        os.rename(origen, destino)
                        print(f"✓ {original}  →  {destino_nombre}")
                        # Si es recursivo, entrar al destino ya renombrado
                        if recursivo:
                            renombrar_directorios(destino, recursivo, dry_run)
                    except OSError as e:
                        print(f"✗ Error renombrando '{original}': {e}")

    except FileNotFoundError:
        print(f"Ruta no encontrada: {path}")
    except PermissionError:
        print(f"Permiso denegado en: {path}")

def main():
    parser = argparse.ArgumentParser(
        description="Renombra carpetas a minúsculas y reemplaza espacios por '_' (snake_case). "
                    "Deja intactas las puramente numéricas."
    )
    parser.add_argument("ruta", nargs="?", default=".", help="Directorio a procesar (por defecto, actual).")
    parser.add_argument("-r", "--recursivo", action="store_true", help="Procesar subdirectorios recursivamente.")
    parser.add_argument("--dry-run", action="store_true", help="Solo mostrar lo que haría sin aplicar cambios.")
    args = parser.parse_args()

    renombrar_directorios(args.ruta, recursivo=args.recursivo, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
