from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from UI.indicators import print_prompt, print_warning, print_success


def get_key():
    key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'key.txt')
    if os.path.exists(key_path):
        with open(key_path, "r") as file:
            return file.read().strip().encode()
    else:
        while True:
            key = input(print_prompt("Enter an encryption/decryption key (32 characters): "))
            if len(key) != 32:
                print_warning("Please input a 32 character key.")
            else:
                break
        with open(key_path, "w") as file:
            file.write(key)
        print_success(f"Encryption/decryption key saved to {key_path}")
        return key.encode()


key = get_key()


def encrypt(data: bytes):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(data) + encryptor.finalize()
    return b64encode(iv + ct)


def decrypt(data: bytes):
    data = b64decode(data)
    iv = data[:16]
    ct = data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ct) + decryptor.finalize()
