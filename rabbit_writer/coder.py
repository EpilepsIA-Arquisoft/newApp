import json
import base64
import hmac
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Claves secretas
KEY = b'abcdefghijklmnop'  # AES key (16 bytes)
HMAC_KEY = b'supersecretkey123'  # HMAC key

IV = b'0000000000000000'  # Vector de inicialización

def load_keys(file_path="rabbit_writer/keys.json"):
    #with open(file_path, "r") as f:
    #    keys_data = json.load(f)

    keys = {
        "KEY": KEY,
        "HMAC_KEY": HMAC_KEY,
        "IV": IV
    }
    return keys

def encrypt_json(data, keys=None):
    keys = load_keys()
    # Convertir diccionario a string JSON
    json_str = json.dumps(data)

    # Cifrar con AES-CBC
    cipher = AES.new(keys["KEY"], AES.MODE_CBC, keys["IV"])
    encrypted_bytes = cipher.encrypt(pad(json_str.encode(), AES.block_size))
    encrypted_base64 = base64.b64encode(encrypted_bytes).decode()

    # Generar HMAC SHA-256 para verificar integridad
    hmac_signature = hmac.new(keys["HMAC_KEY"], encrypted_bytes, hashlib.sha256).hexdigest()

    # Retornar como JSON string
    return json.dumps({
        "data": encrypted_base64,
        "hmac": hmac_signature
    })