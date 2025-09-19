#!/usr/bin/env python3
import os
import re
import sys
import argparse

SPACE_RE = re.compile(r"\s+")
NUM_PREFIX_RE = re.compile(r"^\d+[-_]*")  # detecta prefijos tipo 01-, 02_, etc.

def es_puramente_numerica(nombre: str) -> bool:
    base, _ = os.path.splitext(nombre)
    return base.isdigit()

def transformar_nombre(nombre: str) -> str:
    base, ext = os.path.splitext(nombre)

    # 1. Quitar prefijo numérico (ej: 01-, 02_, 03 )
    base = NUM_PREFIX_RE.sub("", base)

    # 2. minúsculas + espacios a "_"
    base = SPACE_RE.sub("_", base.strip().lower())

    return base + ext.lower()

def renombrar_archivos(path=".", recursivo=False, dry_run=False):
    try:
        with os.scandir(path) as it:
            for entry in it:
                if not entry.is_file(follow_symlinks=False):
                    continue

                original = entry.name
                if es_puramente_numerica(original):
                    print(f"Saltando (numérico): {original}")
                    continue

                destino_nombre = transformar_nombre(original)
                origen = os.path.join(path, original)
                destino = os.path.join(path, destino_nombre)

                if destino_nombre == original:
                    continue

                if os.path.exists(destino) and os.path.realpath(origen) != os.path.realpath(destino):
                    print(f"⚠️ Ya existe '{destino_nombre}'. No renombro '{original}'.")
                    continue

                if dry_run:
                    print(f"[DRY-RUN] {original} → {destino_nombre}")
                else:
                    try:
                        os.rename(origen, destino)
                        print(f"✓ {original} → {destino_nombre}")
                    except OSError as e:
                        print(f"✗ Error renombrando '{original}': {e}")

        if recursivo:
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_dir(follow_symlinks=False):
                        renombrar_archivos(os.path.join(path, entry.name), recursivo, dry_run)

    except FileNotFoundError:
        print(f"Ruta no encontrada: {path}")
    except PermissionError:
        print(f"Permiso denegado: {path}")

def main():
    parser = argparse.ArgumentParser(
        description="Renombra archivos a minúsculas, snake_case y quita prefijos numéricos."
    )
    parser.add_argument("ruta", nargs="?", default=".", help="Directorio a procesar (por defecto, actual).")
    parser.add_argument("-r", "--recursivo", action="store_true", help="Procesar subdirectorios recursivamente.")
    parser.add_argument("--dry-run", action="store_true", help="Solo mostrar cambios sin aplicar.")
    args = parser.parse_args()

    renombrar_archivos(args.ruta, recursivo=args.recursivo, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
