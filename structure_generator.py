import os
import argparse
from pathlib import Path

def mostrar_banner():
    print("""          
     GENERADOR DE ESTRUCTURAS DE DIRECTORIOS
          
    Instrucciones:
    !!. Archivo 'estructura.txt' debe existir en la ruta origen
    1. Primero pegue la ruta de la estructura.
    2. Luego la ruta objetivo, donde va a ser creada la estructura.
    3. Para finalizar Y o N, para saber si es un proyecto Python o no.
    !!. Si es proyecto Python se crean los (__init__.py) y si no lo es, se crean los .gitkeep
    """)

def es_linea_de_formato(linea):
    return all(c in ['│', ' ', '├', '└', '─'] for c in linea.strip())

def crear_archivo_especial(directorio, es_python):
    """Crea __init__.py o .gitkeep según corresponda"""
    archivo = "__init__.py" if es_python else ".gitkeep"
    ruta_archivo = directorio / archivo
    
    if not ruta_archivo.exists():
        with open(ruta_archivo, 'w') as f:
            if es_python:
                f.write("# Package initialization\n")
        print(f"📄 Creado: {ruta_archivo}")

def parse_line(line):
    line = line.strip()
    if not line or es_linea_de_formato(line):
        return None, None, False

    line = line.split('#')[0].strip()
    
    is_file = False
    if '.' in line:
        parts = line.split('── ')
        if len(parts) > 1 and '.' in parts[-1] and '/' not in parts[-1]:
            is_file = True

    indent = 0
    while line.startswith(('    ', '│   ', '├── ', '└── ')):
        line = line[4:]
        indent += 1

    dir_name = line.split('── ')[-1].strip().rstrip('/')
    level = indent if indent > 0 else 0
    return level, dir_name, is_file

def crear_estructura(archivo_estructura, destino, es_python):
    try:
        with open(archivo_estructura, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f]

        root_line = next(line for line in lines if line.strip() and not es_linea_de_formato(line))
        root_dir = root_line.split('#')[0].strip().rstrip('/')
        base_path = Path(destino) / root_dir
        base_path.mkdir(parents=True, exist_ok=True)
        crear_archivo_especial(base_path, es_python)
        print(f"\n🎯 Directorio base creado: {base_path}")

        levels = {0: base_path}
        for line in lines[1:]:
            if es_linea_de_formato(line):
                continue

            level, dir_name, is_file = parse_line(line)
            
            if not dir_name or is_file:
                if is_file:
                    print(f"📄 Archivo ignorado: {dir_name}")
                continue

            if level < 0 or (level - 1) not in levels:
                print(f"⚠️  Estructura inválida en: {line}")
                continue

            parent_dir = levels[level - 1]
            full_path = parent_dir / dir_name
            
            try:
                full_path.mkdir(exist_ok=True)
                crear_archivo_especial(full_path, es_python)
                levels[level] = full_path
                print(f"📂 {full_path}")
            except Exception as e:
                print(f"❌ Error en {dir_name}: {str(e)}")

    except Exception as e:
        print(f"\n🔥 Error crítico: {str(e)}")
        raise

def main():
    mostrar_banner()
    print("\n💡 Ingrese las rutas:")
    origen = input("📍 Ruta al directorio con estructura.txt: ").strip('"')
    destino = input("🎯 Ruta destino para crear la estructura: ").strip('"')

    # Validar tipo de proyecto
    while True:
        tipo = input("¿Es proyecto Python? [Y/N]: ").upper()
        if tipo in ['Y', 'N']:
            es_python = (tipo == 'Y')
            break
        print("❌ Error: Ingrese Y o N")

    origen_path = Path(origen)
    destino_path = Path(destino)
    archivo_estructura = origen_path / "estructura.txt"

    if not archivo_estructura.exists():
        print(f"\n❌ Archivo no encontrado: {archivo_estructura}")
        return

    print(f"\n🚀 Iniciando creación en: {destino_path}")
    crear_estructura(archivo_estructura, destino_path, es_python)
    print("\n✅ ¡Estructura creada con éxito! 🎉")


if __name__ == "__main__":
    main()