import os

def visible_files_iterator(dir_path):
    """
    Generator function that yields items in the given directory path,
    skipping items that start with a dot ('.').
    """
    for item in os.listdir(dir_path):
        if not item.startswith('.'):
            yield item