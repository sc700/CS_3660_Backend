class User:
    def __init__(self, username: str, name: str, password_hash: str):
        self.username = username
        self.name = name        
        self.password_hash = password_hash