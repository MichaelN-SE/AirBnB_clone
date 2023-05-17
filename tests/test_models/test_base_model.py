#!/usr/bin/python3
"""Test of BaseModel class"""
import io
import os
import unittest
from models import storage
from models.base_model import BaseModel
from datetime import datetime


class TestBaseModel_insatiation(unittest.TestCase):
    """For instatiation of class test"""

    def test_no_args(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_created_obj_stored(self):
        self.assertIn(BaseModel(), storage.all().values())

    def test_id_is_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_str(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_difference(self):
        test1 = BaseModel()
        test2 = BaseModel()
        self.assertNotEqual(test1, test2)
        self.assertNotEqual(test1.id, test2.id)
        self.assertNotEqual(test1.created_at, test2.created_at)
        self.assertNotEqual(test1.updated_at, test2.updated_at)

    def str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        tested = BaseModel()
        tested.id = "123"
        tested.created_at = dt
        tested.updated_at = dt
        strtested = tested.__str__()
        string = "[BaseModel] (123)"
        self.assertIn(string, strtested)
        self.assertIn("'id': '123'", strtested)
        self.assertIn("'created_at': " + dt_repr, strtested)
        self.assertIn("'updated_at': ", + dt_repr, strtested)

    def test_with_None_arg(self):
        tested = BaseModel(None)
        self.assertNotEqual(tested.id, None)
        self.assertNotEqual(tested.created_at, None)
        self.assertNotEqual(tested.updated_at, None)

    def test_with_kwargs_None(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        tested = BaseModel(id="123", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(tested.id, "123")
        self.assertEqual(tested.created_at, dt)
        self.assertEqual(tested.updated_at, dt)

    def test_kwargs_with_args(self):
        dt = datetime.today()
        d_iso = dt.isoformat()
        tested = BaseModel("12", id="123", created_at=d_iso, updated_at=d_iso)
        self.assertEqual(tested.id, "123")
        self.assertEqual(tested.created_at, dt)
        self.assertEqual(tested.updated_at, dt)


class test_BaseMode_save(unittest.TestCase):
    """testing the save method in BaseModel class"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "temp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("temp", "file.json")
        except IOError:
            pass

    def test_save(self):
        saved = BaseModel()
        saved.save()
        self.assertLess(saved.created_at, saved.updated_at)

    def test_saved_in_file(self):
        tested = BaseModel()
        tested.save()
        key = "BaseModel." + tested.id
        with open("file.json", "r") as f:
            self.assertIn(key, f.read())

    def test_with_args(self):
        base = BaseModel()
        with self.assertRaises(TypeError):
            base.save(None)

    def test_mul_saves(self):
        base = BaseModel()
        base.save()
        update = base.updated_at
        base.save()
        self.assertLess(update, base.updated_at)


class test_BaseModel_to_dict(unittest.TestCase):
    """Test the dictionary method in BaseModel class"""

    def test_type(self):
        tested = BaseModel()
        self.assertTrue(dict, type(tested.to_dict()))

    def test_items_in_dict(self):
        base = BaseModel()
        self.assertIn("id", base.to_dict())
        self.assertIn("created_at", base.to_dict())
        self.assertIn("updated_at", base.to_dict())
        self.assertIn("__class__", base.to_dict())

    def test_wit_added_attributes(self):
        base = BaseModel()
        base.name = "Florence"
        base.age = 89
        self.assertIn("id", base.to_dict())
        self.assertIn("created_at", base.to_dict())
        self.assertIn("updated_at", base.to_dict())
        self.assertIn("name", base.to_dict())
        self.assertIn("age", base.to_dict())

    def test_to_dict_with_args(self):
        base = BaseModel()
        with self.assertRaises(TypeError):
            base.to_dict(None)

    def test_dict(self):
        base = BaseModel()
        base.id = "1234"
        dt = datetime.today()
        base.created_at = base.updated_at = dt
        dicti = {
            "id": "1234",
            "__class__": 'BaseModel',
            "created_at": dt.isoformat(),
            "updated_at": dt.isoformat()
        }
        self.assertDictEqual(dicti, base.to_dict())

    def test_to_dict_anddict(self):
        bm = BaseModel()
        self.assertNotEqual(bm.to_dict(), bm.__dict__)


if __name__ == "__main__":
    unittest.main()
