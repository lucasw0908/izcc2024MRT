from sqlalchemy import Column, Integer, String, Boolean

from . import db


class Users(db.Model):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True, nullable=False)
    password = Column(String(64), nullable=False)
    is_admin = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<User {self.username}>"