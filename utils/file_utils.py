import os

def get_pathname_without_extension(full_path):
    # Split the full path into pathname and extension
    pathname, _ = os.path.splitext(full_path)
    
    # Get only the filename without the extension from the pathname
    filename_without_extension = os.path.basename(pathname)
    
    return filename_without_extension

def get_filename_from_full_path(full_path):
    return os.path.basename(full_path)
