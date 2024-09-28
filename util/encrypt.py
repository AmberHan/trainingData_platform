from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64


def encrypt_pwd(pwd: str) -> str:
    common_iv = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    encrypt_key = b'beijingcompanybasicvideoanalysis'

    pwd_bytes = pwd.encode('utf-8')

    cipher = Cipher(algorithms.AES(encrypt_key), modes.CFB(common_iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(pwd_bytes) + encryptor.finalize()

    pwd_str = base64.b64encode(ciphertext).decode('utf-8')
    return pwd_str
