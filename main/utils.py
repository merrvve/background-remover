import sys
import os      


def resource_path(relative_path1,relative_path2):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path1, relative_path2)

def hex_to_rgba(hex_string):
    if hex_string:
        # Remove '#' from the beginning of the string, if present
        if hex_string.startswith('#'):
            hex_string = hex_string[1:]

        # Convert hexadecimal string to RGB values
        r = int(hex_string[0:2], 16)
        g = int(hex_string[2:4], 16)
        b = int(hex_string[4:6], 16)

        # Set alpha value (standard value)
        a = 255  # Assuming the alpha value is 255 (fully opaque)

        # Return RGBA tuple
        return (r, g, b, a)
    else:
        return None

