#!/usr/bin/python3
"""Defines BaseModel Class"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """Class about the base model"""

    def __init__(self, *args, **kwargs):
        """Initializes the class"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) > 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.fromisoformat(value)
                elif key != "__class__":
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

    def save(self):
        """Method to save"""
        self.updated_at = datetime.today()
        models.storage.save()

    def __str__(self):
        """Return the str representation of the base model"""
        k = self.__class__.__name__
        return "[{}] ({}) {}".format(k, self.id, self.__dict__)

    def to_dict(self):
        """returns dictionary containing all key, values of __dict__"""
        dict = self.__dict__.copy()
        dict["__class__"] = self.__class__.__name__
        dict["created_at"] = self.created_at.isoformat()
        dict["updated_at"] = self.updated_at.isoformat()
        return dict
