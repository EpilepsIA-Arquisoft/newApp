
from google.cloud import storage
import os
from .check import check
from .delete import delete

def upload(examen_id, direccion_archivo_local, GCS_BASE_FOLDER):
    """
    Sube un archivo de examen al bucket de Google Cloud Storage.

    :param nombre_examen: Nombre con el que se guardará el archivo en el bucket (sin carpeta base).
    :param direccion_archivo_local: Ruta local del archivo que deseas subir.
    :return: URL pública del archivo subido.
    """
    GCS_BUCKET_NAME = "examenes-eeg"

    check()

    destino_en_bucket = os.path.join(GCS_BASE_FOLDER).replace("\\", "/")

    # Inicializar cliente GCS (usando variables de entorno ya definidas)
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(destino_en_bucket)

    # Precondición: asegura que no sobreescriba un archivo existente accidentalmente
    generation_match_precondition = 0

    # Subir archivo
    blob.upload_from_filename(direccion_archivo_local, if_generation_match=generation_match_precondition)
    
    url = f"https://storage.googleapis.com/{GCS_BUCKET_NAME}/{GCS_BASE_FOLDER}/{examen_id}"
    
    delete(direccion_archivo_local)

    return url
