""" This contains all of the utility functions used throughout
the ACOReader project.

"""
__package__ = 'acoreader'


from ctypes import pointer, memmove, sizeof
import os
import sys
from ctypes import c_uint16, c_int16, c_uint32
from io import BytesIO
from typing import Optional


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
        _c = file.read(2)
        if sys.byteorder == 'little':
          _c = _c[::-1]
          _r += _c.decode('UTF16')
    # We'll make sure that we don't return any null characters that
    # might be in the file.
    return _r.replace('\0', '')
