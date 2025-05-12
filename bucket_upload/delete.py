import os

def delete( nombre_archivo, ruta_carpeta='bucket/examenes_temp'):
    """
    Borra un archivo dentro de una carpeta.

    :param ruta_carpeta: Ruta absoluta o relativa de la carpeta.
    :param nombre_archivo: Nombre del archivo a borrar (incluyendo extensión).
    """
    ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)

    if os.path.exists(ruta_archivo):
        os.remove(ruta_archivo)
        print(f"Archivo '{nombre_archivo}' borrado correctamente.")
    else:
        print(f"El archivo '{nombre_archivo}' no existe en '{ruta_carpeta}'.")

# Ejemplo de uso:
# borrar_archivo('bucket', 'upload.py')
