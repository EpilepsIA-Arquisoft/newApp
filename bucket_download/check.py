from google.cloud import storage

def check_bucket(nombre_bucket):
    """
    Verifica si un bucket existe en Google Cloud Storage.
    :param nombre_bucket: Nombre del bucket a verificar.
    :return: True si existe y es accesible, False si no existe o no tienes permiso.
    """
    from google.api_core.exceptions import NotFound, Forbidden
    
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(nombre_bucket)
        print(f"El bucket '{nombre_bucket}' existe y es accesible.")
        return True
    except NotFound:
        print(f"El bucket '{nombre_bucket}' no existe.")
        return False
    except Forbidden:
        print(f"No tienes permisos para acceder al bucket '{nombre_bucket}'.")
        return False
    except Exception as e:
        print(f"Error al verificar el bucket: {e}")
        return False

def check_credentials(nombre_archivo_credenciales="jjdc-453414-7962ee87f1a0.json"):
    """
    Verifica si las credenciales de GCP están activas.
    Si no, busca el archivo JSON en la misma carpeta y lo activa.
    :param nombre_archivo_credenciales: Nombre del archivo JSON con la cuenta de servicio.
    :return: True si las credenciales están listas, False si no se pudieron establecer.
    """
    from google.auth.exceptions import DefaultCredentialsError
    import os

    try:
        # Intentar inicializar un cliente de prueba para verificar credenciales
        storage.Client().list_buckets()
        return True

    except DefaultCredentialsError:
        # Obtener la ruta del archivo .py actual
        ruta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_credenciales = os.path.join(ruta_actual, nombre_archivo_credenciales)

        if not os.path.exists(ruta_credenciales):
            return False

        # Establecer la variable de entorno
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ruta_credenciales

        try:
            # Probar nuevamente
            storage.Client().list_buckets()
            return True
        except Exception as e:
            return False
        
def check():
    if not check_credentials():
        raise RuntimeError("Las credenciales no están listas o no se pudieron establecer.")
    if not check_bucket("examenes-eeg"):
        raise RuntimeError("El bucket 'examenes-eeg' no existe o no es accesible.")
    return