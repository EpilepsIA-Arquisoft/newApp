import os
from google.cloud import storage

from check import check

def download(url_examen: str, destino_local="bucket_download/examenes_temp/"):
    check()
    """
    Descarga un archivo desde una URL pública de Google Cloud Storage y lo guarda en la ruta destino_local.

    :param url_examen: URL pública del examen en Google Cloud Storage.
    :param destino_local: Ruta local donde se guardará el archivo descargado.
    """
    # Validar URL
    if "https://storage.googleapis.com/" not in url_examen:
        raise ValueError("La URL proporcionada no es válida para Google Cloud Storage.")

    # Obtener el nombre del bucket y el blob path desde la URL
    url_parts = url_examen.replace("https://storage.googleapis.com/", "").split("/")
    if len(url_parts) != 3:
        raise ValueError("La URL no tiene el formato esperado.")

    bucket_name, _, blob_name = url_parts

    # Inicializar cliente de GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(_+"/"+blob_name)

    # Descargar el archivo al destino local
    blob.download_to_filename(destino_local+blob_name)

    print(destino_local+"/"+blob_name)

download("https://storage.googleapis.com/examenes-eeg/completos/examen_1.edf")