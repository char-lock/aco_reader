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
__package__ = 'acoreader'


import os
import sys
from io import BytesIO
from typing import Callable, Optional
from _types import *

from .util import (
  read_uint16, read_uint32,
  read_int16, read_string
)


def decode_rgb(values: list[int]) -> list[float]:
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


def decode_hsb(values: list[int]) -> list[float]:
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


def decode_cmyk(values: list[int]) -> list[float]:
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


def decode_lab(values: list[int]) -> list[float]:
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


def interpret_colors(color_space: ColorSpace, values: list[int]) -> str:
    """ Interprets the provided color values according to the rules of
    the provided color space.


    #### Parameters

    * color_space: ColorSpace
        * the color space by which to interpret the values
        * see https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/#50577411_22664

    * values: list[int]
        * a list of values to be converted according to the color space.
        * must be at least three values long


    #### Returns
      * List[float]
          * a list containing the `values` interpreted by the rules
            pertaining to `color_space`

    """
    if (len(values) < 3):
        err: str = 'Too few values provided to interpret color values.'
        err += f'\n    Got {len(values)}, should be at least 3.'
        raise ValueError(err)
    decode_methods: Dict[ColorSpace, Callable] = {
      ColorSpace.RGB: decode_rgb,
      ColorSpace.HSB: decode_hsb,
      ColorSpace.CMYK: decode_cmyk,
      ColorSpace.LAB: decode_lab
    }
    if (color_space not in decode_methods.keys()):
      err: str = 'The color space provided cannot be interpreted. \n'
      err += f'    color_space = {color_space.name}'
      raise ValueError(err)
    else:
      return decode_methods[color_space](values)


def read_color_values(file: BytesIO) -> ColorSwatch:
    """ Reads the color values from `file`, interprets them, and returns
    a ColorSwatch that can be written to a file.


    #### Parameters

    * file: BytesIO
        * input stream from a file from which to read the next color
          values


    #### Returns

    * ColorSwatch
        * a ColorSwatch object containing the definition of the next
          swatch in `file`

    """
    color_space_val: int = read_uint16(file)
    color_space: ColorSpace = ColorSpace.from_value(color_space_val)
    c_val_0: int = read_uint16(file)
    # Check for the color space, as some will need signed values, and
    # others use unsigned.
    c_val_1: int = 0
    c_val_2: int = 0
    c_val_3: int = 0
    if (color_space.value == 7):
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
    values: List[float] = interpret_colors(
        color_space,
        [c_val_0, c_val_1, c_val_2, c_val_3]
    )
    return ColorSwatch(
        s_name,
        color_space, 
        values
    )


def read_file(filename: str, xargs: Optional[dict] = None) -> None:
    """ Reads a the file indicated by `filename` and writes the
    interpreted data to a text file.


    #### Parameters

    * filename: str
        * the path to the target .aco file to read

    * args: Optional[dict]
        * a dictionary containing optional arguments

    """
    # Process through any arguments provided.
    verbose: bool = False
    fail_quiet: bool = False
    if xargs is not None:
        if (os.path.sep == xargs['input_directory'][-1]):
            filename = xargs['input_directory'] + filename
        else:
            filename = xargs['input_directory'] + os.sep + filename
            verbose = xargs['verbose']
            fail_quiet = xargs['fail_quiet']
    # Open the file in as raw bytes.
    _f: BytesIO = open(filename, 'rb')
    # Check the file version.
    version: int = read_uint16(_f)
    if (version != 2):
        if (fail_quiet):
            # If we are meant not to show errors to the user, we will
            # just fail quietly.
            return
        else:
            err: str = 'This script is currently unable to process .aco'
            err += ' files of any version other than 2. \n'
            err += f'    version = {version}'
            raise ValueError(err)
    # Get color count.
    color_count: int = read_uint16(_f)
    if (verbose):
        print(f'Reading {color_count} colors from \'{filename}\' ...')
    # Process all of the colors.
    if (fail_quiet):
        fail_count: int = 0
    for _ in range(color_count):
        try:
            _wr: ColorSwatch = read_color_values(_f)
        except ValueError as ex:
            if (fail_quiet):
                fail_count += 1
                continue
            else:
                raise ex
        with open(
            filename[:-4].replace(
                xargs['input_directory'], xargs['output_directory']
            ) + '.txt', 'a+', encoding=sys.getdefaultencoding()
         ) as out:
            out.write(str(_wr))
    if (verbose):
        print(f"Finished reading '{filename}'. Results saved in '{filename[:-4]}.txt'.")
        if (fail_quiet):
            print(f'Failed to interpret {fail_count} swatches.')
