# src/file_operations.py

import os
import shutil

def create_file(path):
    with open(path, 'w') as f:
        pass

def rename_file(src, dest):
    os.rename(src, dest)

def delete_file(path):
    os.remove(path)

def copy_file(src, dest):
    shutil.copy(src, dest)

def create_directory(path):
    os.makedirs(path)

def delete_directory(path):
    shutil.rmtree(path)
