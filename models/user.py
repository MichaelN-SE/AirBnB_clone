#!/usr/bin/python3
"""Module on user class."""
from models.base_model import BaseModel



class User(BaseModel):
    """Class user"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
