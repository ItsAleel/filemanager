import os

def is_image_file(path):
    return path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))

def is_text_file(path):
    return not is_image_file(path)
