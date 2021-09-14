import os

# Get absolute path from the calling function
def get_absolute_path(path):
    return os.path.abspath(path)

def get_relative_path_from_utils(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
