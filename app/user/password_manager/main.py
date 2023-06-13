import hashlib


class PasswordGenerator:
    def __init__(self):
        self.obj = hashlib.sha256

    def hash_password(self, password: bytes) -> str:
        hash_obj = self.obj()
        hash_obj.update(password)
        return hash_obj.hexdigest()
