#ChatGPT wrote this shit, all credit to ChatGPT, sorry I tried
from cryptography.fernet import Fernet

class SecureProtocol:
    def __init__(self, key: str = None):
        if key is not None:
            self.key = key.encode('utf-8')
        else:
            self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def get_key(self) -> str:
        return self.key.decode('utf-8')

    def encrypt(self, data: str) -> bytes:
        return self.cipher.encrypt(data.encode('utf-8'))

    def decrypt(self, token: bytes) -> str:
        return self.cipher.decrypt(token).decode('utf-8')
