import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_file_path(relative_path):
    return os.path.join(PROJECT_DIR, relative_path)