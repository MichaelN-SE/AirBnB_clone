#!/usr/bin/python3
"""calls filestorage class"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
