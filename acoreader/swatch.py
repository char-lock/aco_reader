""" This module interprets a text file formatted in the same way
ACOReader exports ColorSwatches.

"""
__package__ = 'acoreader'


from io import TextIOWrapper
from ._types import *

def read_next_swatch(file: TextIOWrapper) -> ColorSwatch:
    """ Reads the next swatch from a provided file. 
    

    #### Parameters
    * file: TextIOWrapper
        * File from which to read the next swatch


    #### Returns
    * ColorSwatch
        * The next defined color swatch
    
    """
    # Continue reading lines until we find one that matches
    # 'ColorSwatch {', which indicates the start of a new swatch.
    _line: str = file.readline()
    while ('ColorSwatch' not in _line):
        _line = file.readline()
    # Once the loop is escaped, we know that we can start to read
    # the color swatch information.
    # ColorSwatch -> Name
    _name: str = file.readline()
    _name = _name.replace('name:', '').replace('\'', '')
    name:str = _name.replace(',', '').strip()
    _name = None
    # ColorSwatch -> color_space
    _color_space: str = file.readline()
    _color_space.replace('color_space:', '').replace(',', '').strip()
    color_space: ColorSpace = ColorSpace.from_name(_color_space)
    # We'll skip the next line because it only really indicates that
    # the values are starting.
    _ = file.readline()
    # We'll make sure that we know how to handle the particular color
    # space for this swatch.
    if color_space.value in [-1, 3, 4, 5, 6, 10]:
        err: str = 'This swatch is defined with an unimplemented '
        err += f'color space.\n    color_space = {color_space.name}'
        raise ValueError(err)
    # Now, we'll check how many values we should be pulling.
    value_sz: int = 3
    if color_space == ColorSpace.CMYK:
        value_sz = 4
    elif color_space == ColorSpace.GRAYSCALE:
        value_sz = 1
    values: List[float] = []
    # Now we'll pull each value and put it into a list.
    for i in range(value_sz):
        _v: str = file.readline(1)
        _v = _v.replace(COLOR_SPACE_LABELS[color_space][i].lower(), '')
        _v = _v.replace(':', '').strip()
        values.append(float(_v))
    # We'll go ahead and read the next two lines just to get the
    # closing brackets out of the way.
    file.readline()
    file.readline()
    # We have all of the information we need to create the ColorSwatch
    # object and return it.
    return ColorSwatch(name, color_space, values)

