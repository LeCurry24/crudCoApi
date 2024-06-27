from .base import Base

class Users(Base, table=True):
    __tablename__ = "users"
