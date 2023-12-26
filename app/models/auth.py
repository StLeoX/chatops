# Flask modules
from flask_login import UserMixin

# Other modules
from datetime import datetime

# Local modules
from app.extensions.db import db
    

class User(UserMixin):
    # TODO: 尝试在配置文件中设置
    TTL = 600  # 10 minutes in seconds

    def __init__(self, name=None, key=None):
        self.name = name
        self.key = key
        self.redis = db

        if name and key:
            self.save(self.name, self.key)

    def username_exists(self):
        return self.redis.exists(f'user:{self.name}')

    def save(self, name=None, key=None):
        if self.username_exists():
            raise ValueError("Username already exists")
        if name and key:
            # Using setex to set the value and the TTL together
            self.redis.setex(f'user:{name}', User.TTL, str(key))

    def get(self):
        key = self.redis.get(f'user:{self.name}')
        if key:
            return key
        return None
    
    def load(self, name):
        self.name = name
        self.key = self.get()
    
    def is_authenticated(self):
        return self.username_exists()

    def delete(self):
        self.redis.delete(f'user:{self.name}')

    def get_id(self):
        return self.name

    def __repr__(self):
        return f"<User {self.name, self.key} >"

