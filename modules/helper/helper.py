

def check_file_naming(filename: str, extension: str) -> str:
    """checks filename for extension
    appends extension if it's not there
    """

    if filename.endswith(extension):
        return filename
    else:
        filename = filename.split(".", 1)[0]
        return filename + extension
