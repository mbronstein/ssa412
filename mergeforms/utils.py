#utils.py
import os
from tempfile import NamedTemporaryFile
import requests
import time

# Tempfile related

def save_string_to_tempfile(body, dir=None,
                            output_filepath=None,
                            prefix=None,
                            suffix=None,
                            mode=None):
    """
        create temp file , fill it with string and return the file path
        if filepath not provided, create tempfile, same for dir
        Arguments:
            str:
            dir:
        Returns:
            filepath to file
    """
    if output_filepath:

        with open(output_filepath, "w") as f:
            f.write(body)
            return output_filepath
    else:
        if not mode:
            mode = "w"

        temp_file = NamedTemporaryFile(dir=dir,delete=False, mode=mode, prefix=prefix, suffix=suffix )
        temp_file.write(body)
        temp_file.close()
        print("Tempfilename: " + temp_file.name)
        return temp_file.name





# pdf related utilities





#
def open_local_or_remote_file(file_uri):
    """
    read the template file as local file or if remote URL convert it to a temp. local file
    Args:
        uri: str

    Returns:

    """
    if file_uri.upper().startswith("HTTP"):
            try:
                file_body = requests.get(file_uri)
            except Exception as e:
               raise Exception("Error retrieving {0}: {1}".format(file_uri, str(e)))
    elif not os.path.exists(file_uri):
            raise  Exception("error finding template file: {0}".format(file_uri))
    else:
        try:
            with open(file_uri,"r") as f:
                file_body = f.read()
        except Exception as e:
            raise Exception("Error opening template file: {0}".format(file_uri))
    return file_body


def seconds_since_midnight():
    now = time.localtime()
    seconds  = now.tm_hour*60*60+now.tm_min*60+ now.tm_sec
    return str(seconds)

