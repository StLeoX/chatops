# Flask modules
from flask_login import UserMixin

# Other modules
from datetime import datetime

# Local modules
from app.extensions.db import db
    

class User(UserMixin):
    def __init__(self, name=None, key=None):
        self.name = name
        self.key = key
        self.redis = db

        if name and key:
            self.save(self.name, self.key)

    def username_exists(self):
        return self.redis.hexists('users', self.name)

    def save(self, name=None, key=None):
        # TODO: Save id without name?
        if self.username_exists():
            raise ValueError("Username already exists")
        if name and key:
            self.redis.hset('users', str(name), str(key))

    def get(self):
        key = self.redis.hget('users', self.name)
        if key:
            return key
        return None
    
    def load(self, name):
        self.name = name
        self.key = self.get()
    
    def is_authenticated(self):
        if self.redis.hexists('users', self.name):
            return True
        return False

    def delete(self):
        self.redis.hdel('users', self.name)

    def get_id(self):
        return self.name

    def __repr__(self):
        return f"<User {self.id, self.name}>"

