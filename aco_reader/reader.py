""" Handles reading aco files and interpreting the color swatch data
encoded inside.

"""
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <https://unlicense.org>
#
from io import BytesIO
import os
import sys
from typing import Optional
from ctypes import c_uint16, c_int16, c_uint32, pointer, memmove, sizeof


def read_uint16(file: BytesIO) -> int:
    """ Reads an unsigned 16-bit integer from `file` and returns it as
    an int.


    #### Parameters
    * file: BytesIO
      * input stream from a file from which to read


    #### Returns
    * int
      * the 16-bit unsigned integer as an int

    """
    # Read two bytes from the file; .aco files are in big-endian order,
    # so we need to check whether or not we need to flip the bits.
    _c: bytes = file.read(2)
    if (sys.byteorder == 'little'):
      _c = _c[::-1]
    # Convert the read bytes straight to an integer.
    _v: c_uint16 = c_uint16(0)
    memmove(pointer(_v), _c, sizeof(c_uint16))
    return _v.value

def read_int16(file: BytesIO) -> int:
    """ Reads a signed 16-bit integer from `file` and returns it as
    an int.


    #### Parameters
    * file: BytesIO
      * input stream from a file from which to read


    #### Returns
    * int
      * the signed 16-bit integer as an int

    """
    # Read two bytes from the file; .aco files are in big-endian order,
    # so we need to check whether or not we need to flip the bits.
    _c: bytes = file.read(2)
    if (sys.byteorder == 'little'):
      _c = _c[::-1]
    # Convert the read bytes straight to an integer.
    _v: c_int16 = c_int16(0)
    memmove(pointer(_v), _c, sizeof(c_int16))
    return _v.value


def read_uint32(file: BytesIO) -> int:
    """ Reads an unsigned 32-bit integer from `file` and returns it as
    an int.


    #### Parameters

    * file: BytesIO
        * input stream from a file from which to read


    #### Returns

    * int
      * the 32-bit integer as an int

    """
    # Read two bytes from the file; .aco files are in big-endian order,
    # so we need to check whether or not we need to flip the bits.
    _c: bytes = file.read(4)
    if (sys.byteorder == 'little'):
      _c = _c[::-1]
    # Convert the read bytes straight to an integer.
    _v: c_uint32 = c_uint32(0)
    memmove(pointer(_v), _c, sizeof(c_uint16))
    return _v.value


def read_string(file: BytesIO, length: int) -> str:
    """ Reads a string from `file` of size `length` and returns it.


    #### Parameters

    * file: BytesIO
      * input stream from a file from which to read

    * length: int
      * length of string in bytes


    #### Returns

    * str
      * the next string of `length` length from `file`

    """
    _r: str = ''
    for _ in range(length):
        _r += file.read(2).decode()
    return _r.replace('\0', '')


def get_rgb(values: list[int]) -> list[float]:
    """ Returns a list of values for an RGB color definition.


    #### Parameters

    * values: list[int]
      * a list containing a minimum of 3 values
      * it is assumed that all values are retrieved via read_int16


    #### Returns
    * list[float]
      * a list containing the converted values

    """
    if (len(values) < 3):
        err: str = 'Too few values provided for RGB conversion.\n    '
        err += f'Got {len(values)}, should be at least 3.'
        raise ValueError(err)
    return [(v / 256) for v in values[:3]]


def get_hsb(values: list[int]) -> list[float]:
    """ Returns a list of values for an HSB color definition.


    #### Parameters

    * values: list[int]
      * a list containing a minimum of 3 values
      * it is assumed that all values are retrieved via read_int16


    #### Returns
    * list[float]
      * a list containing the converted values

    """
    if (len(values) < 3):
        err: str = 'Too few values provided for HSB conversion.\n    '
        err += f'Got {len(values)}, should be at least 3.'
        raise ValueError(err)
    return [values[0] / 182.04, values[1] / 655.35, values[2] / 655.35]


def get_cmyk(values: list[int]) -> list[float]:
    """ Returns a list of values for a CMYK color definition.


    #### Parameters

    * values: list[int]
      * a list containing a minimum of 4 values
      * it is assumed that all values are retrieved via read_int16


    #### Returns
    * list[float]
      * a list containing the converted values

    """
    if (len(values) < 4):
        err: str = 'Too few values provided for CMYK conversion.\n    '
        err += f'Got {len(values)}, should be at least 4.'
        raise ValueError(err)
    return [v / 655.35 for v in values]


def get_lab(values: list[int]) -> list[float]:
    """ Returns a list of values for an LAB color definition.


    #### Parameters

    * values: list[int]
      * a list containing a minimum of 3 values
      * it is assumed that all values are retrieved via read_int16


    #### Returns
    * list[float]
      * a list containing the converted values

    """
    if (len(values) < 3):
        err: str = 'Too few values provided for LAB conversion.\n    '
        err += f'Got {len(values)}, should be at least 3.'
        raise ValueError(err)
    return [v / 100 for v in values[:3]]


def interpret_colors(color_space: int, values: list[int]) -> str:
    """ Interprets the provided color values according to the rules of
    the provided color space.


    #### Parameters

    * color_space: int
      * an integer representing a specified color space.
      * see https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/#50577411_22664

    * values: list[int]
      * a list of values to be converted according to the color space.
      * must be at least three values long


    #### Returns
      * str
        * a string in the format prepended with a label for the color
          space, followed by comma-separated converted values.

    """
    if (len(values) < 3):
        err: str = 'Too few values provided to interpret color values.'
        err += f'\n    Got {len(values)}, should be at least 3.'
        raise ValueError(err)
    _col: list[float] = []
    _l: str = ''
    if color_space == 0:
        _l = 'RGB'
        _col.extend(get_rgb(values))
    elif color_space == 1:
        _l = 'HSB'
        _col.extend(get_hsb(values))
    elif color_space == 2:
        _l = 'CMYK'
        _col.extend(get_cmyk(values))
    elif color_space == 7:
        _l = 'LAB'
        _col.extend(get_lab(values))
    else:
        raise ValueError(f"Unhandled color space. color_space = {color_space}")
    return _l + ', ' + ', '.join([f'{c:.2f}' for c in _col])


def read_color_values(file: BytesIO) -> str:
    """ Reads the color values from `file`, interprets them, and returns
    a string that can be written to a file.


    #### Parameters

    * file: BytesIO
      * input stream from a file from which to read the next color
        values


    #### Returns

    * str
      * a string to be written to a text file containing the interpreted
        value for the next color value

    """
    color_space: int = read_uint16(file)
    c_val_0: int = read_uint16(file)
    # Check for the color space, as some will need signed values, and
    # others use unsigned.
    c_val_1: int = 0
    c_val_2: int = 0
    c_val_3: int = 0
    if (color_space == 7):
        # LAB color space uses signed integer values.
        c_val_1 = read_int16(file)
        c_val_2 = read_int16(file)
        c_val_3 = read_int16(file)
    else:
        c_val_1 = read_uint16(file)
        c_val_2 = read_uint16(file)
        c_val_3 = read_uint16(file)
    n_len: int = read_uint32(file)
    s_name: str = read_string(file, n_len)
    col: str = interpret_colors(color_space, [c_val_0, c_val_1, c_val_2, c_val_3])
    return s_name + ", " + col + "\n"


def read_file(filename: str, xargs: Optional[dict] = None) -> None:
    """ Reads a the file indicated by `filename` and writes the
    interpreted data to a text file.


    #### Parameters

    * filename: str
      * the path to the target .aco file to read

    * args: Optional[dict]
      * a dictionary containing optional arguments

    """
    if (os.path.sep == xargs['input_directory'][-1]):
        filename = xargs['input_directory'] + filename
    else:
        filename = xargs['input_directory'] + os.sep + filename
    _f: BytesIO = open(filename, 'rb')
    verbose: bool = xargs['verbose']
    fail_quiet: bool = xargs['fail_quiet']
    # Check the file version.
    version: int = read_uint16(_f)
    if (version != 2):
        if (not fail_quiet):
            raise ValueError(f"This script is currently unable to process .aco files of any version other than 2.\nversion = {version}")
        else:
            return
    # Get color count.
    color_count: int = read_uint16(_f)
    if (verbose):
        print(f"Reading {color_count} colors from '{filename}' ...")
    # Process all of the colors.
    if (fail_quiet):
        fail_count: int = 0
    for _ in range(color_count):
        try:
            _wr: str = read_color_values(_f)
        except ValueError as ex:
            if (fail_quiet):
                fail_count += 1
                continue
            else:
                raise ex
        with open(
          filename[:-4].replace(
            xargs['input_directory'], xargs['output_directory']
          ) + '.txt', 'a+', encoding=sys.getdefaultencoding()) as out:
            out.write(_wr)
    if (verbose):
        print(f"Finished reading '{filename}'. Results saved in '{filename[:-4]}.txt'.")
        if (fail_quiet):
            print(f'Failed to interpret {fail_count} swatches.')
