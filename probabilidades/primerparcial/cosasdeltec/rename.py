#!/usr/bin/env python3
import os
import re
import sys
import argparse

SPACE_RE = re.compile(r"\s+")

def es_puramente_numerica(nombre: str) -> bool:
    # Solo el nombre sin extensión
    base, _ = os.path.splitext(nombre)
    return base.isdigit()

def transformar_nombre(nombre: str) -> str:
    # minúsculas + espacios reemplazados por "_"
    return SPACE_RE.sub("_", nombre.strip().lower())

def renombrar_archivos(path=".", recursivo=False, dry_run=False):
    try:
        with os.scandir(path) as it:
            for entry in it:
                # Solo archivos reales
                if not entry.is_file(follow_symlinks=False):
                    continue

                original = entry.name

                # Ignorar numéricos puros
                if es_puramente_numerica(original):
                    print(f"Saltando (numérico): {original}")
                    continue

                destino_nombre = transformar_nombre(original)
                origen = os.path.join(path, original)
                destino = os.path.join(path, destino_nombre)

                # Si no hay cambios, seguir
                if destino_nombre == original:
                    continue

                # Evitar colisiones
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

        # Procesar subdirectorios si es recursivo
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
        description="Renombra archivos a minúsculas y reemplaza espacios por '_' (snake_case). "
                    "Ignora nombres puramente numéricos."
    )
    parser.add_argument("ruta", nargs="?", default=".", help="Directorio a procesar (por defecto, actual).")
    parser.add_argument("-r", "--recursivo", action="store_true", help="Procesar subdirectorios recursivamente.")
    parser.add_argument("--dry-run", action="store_true", help="Solo mostrar cambios sin aplicar.")
    args = parser.parse_args()

    renombrar_archivos(args.ruta, recursivo=args.recursivo, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
