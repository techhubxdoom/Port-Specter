from cryptography.fernet import Fernet
from dotenv import load_dotenv, set_key
import os
from os import path


class EncryptDecryptData:

    def __init__(self):
        self.ROOT_DIR = path.abspath(path.join(path.dirname(__file__), '..', '..'))
        self.ENV_PATH = path.join(self.ROOT_DIR, '.env')

        self.check_key()

        load_dotenv(self.ENV_PATH)
        self.ENC_KEY = os.getenv("ENC_KEY").encode()

        self.cipher = Fernet(self.ENC_KEY)


    # -------------------------
    def check_key(self):
        if not path.exists(self.ENV_PATH):
            open(self.ENV_PATH, "w").close()

        load_dotenv(self.ENV_PATH)

        if os.getenv("ENC_KEY") is None:
            key = Fernet.generate_key().decode()
            set_key(self.ENV_PATH, "ENC_KEY", key)


    # -------------------------
    def encrypt(self, data: str) -> bytes:
        return self.cipher.encrypt(data.encode())

    def decrypt(self, data: bytes) -> str:
        return self.cipher.decrypt(data).decode()


# x = EncryptDecryptData()

# print(x.decrypt(b'gAAAAABplb_te5XjoxWjDHe2Jh7KtKvE8RVOhEKw1_-B9n3DUeTXJJPNkoi9Bt5Q_ONCbqs1cSau8-ZoDaV8CZPtRwhtIbdriQ=='))
