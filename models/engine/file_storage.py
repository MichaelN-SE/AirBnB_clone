#!usr/bin/python3
"""Model for file storage."""
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.state import State
from models.review import Review
from models.city import City


class FileStorage:
    """Class for file storage."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary objects."""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the  obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to file  path file.json"""
        object_dict = {}
        for key, obj in self.__objects.items():
            object_dict[key] = obj.to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(object_dict, f)

    def reload(self):
        """ deserialize from file.json"""
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                dicti = json.load(f)
            for val in dicti.values():
                clsnm = val["__class__"]
                self.new(eval(clsnm)(**val))

        except FileNotFoundError:
            pass
