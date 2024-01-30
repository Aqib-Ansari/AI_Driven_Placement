from cryptography.fernet import Fernet
from dotenv import load_dotenv

import os

load_dotenv()

def encrypt_password(password):
    cipher_suite = Fernet(b'mG_1wG4aPNPdoLVttI8k_yq5OAAkO8DA6Rsb41-4Sjc=')
    cipher_text = cipher_suite.encrypt(password.encode())
    return cipher_text

def decrypt_password(cipher_text):
    cipher_suite = Fernet(b'mG_1wG4aPNPdoLVttI8k_yq5OAAkO8DA6Rsb41-4Sjc=')
    decrypted_text = cipher_suite.decrypt(cipher_text).decode()
    return decrypted_text


if __name__ == "__main__":
    print(encrypt_password("aqib"))

    print(decrypt_password(encrypt_password("aqib")))