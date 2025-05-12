import json
import base64
import hmac
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def load_keys(file_path="keys.json"):
    with open(file_path, "r") as f:
        keys_data = json.load(f)

    keys = {
        "KEY": base64.b64decode(keys_data["KEY"]),
        "HMAC_KEY": base64.b64decode(keys_data["HMAC_KEY"]),
        "IV": base64.b64decode(keys_data["IV"])
    }
    return keys

def decrypt_json(encrypted_json_str, keys):
    encrypted_json = json.loads(encrypted_json_str)
    encrypted_base64 = encrypted_json["data"]
    received_hmac = encrypted_json["hmac"]

    # Decodificar Base64
    encrypted_bytes = base64.b64decode(encrypted_base64)

    # Verificar integridad HMAC
    expected_hmac = hmac.new(keys["HMAC_KEY"], encrypted_bytes, hashlib.sha256).hexdigest()
    if expected_hmac != received_hmac:
        raise ValueError("Error: La integridad del mensaje ha sido comprometida")

    # Descifrar con AES-CBC
    cipher = AES.new(keys["KEY"], AES.MODE_CBC, keys["IV"])
    decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)

    return json.loads(decrypted_bytes.decode())
