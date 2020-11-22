

def check_filename(filename, extension):
    """checks filename for extension
    appends extension if it's not there
    """

    if filename.endswith(extension):
        return filename
    else:
        filename = filename.split(".", 1)[0]
        return filename + extension