""" This contains all of the utility functions used throughout
the ACOReader project.

"""
__package__ = 'acoreader'


from ctypes import pointer, memmove, sizeof
import os
import struct
import sys
from codecs import encode
from ctypes import c_char, c_uint16, c_int16, c_uint32
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

def to_uint16(val: int) -> bytes:
  """ Returns the uint16 bytes for the provided value. """
  _v: c_uint16 = c_uint16(val)
  _x: bytes = bytes(_v)
  if sys.byteorder == 'little':
    _x = _x[::-1]
  return bytes(_x)

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

def to_int16(val: int) -> bytes:
  """ Returns the int16 bytes for the provided value. """
  _v: c_uint16 = c_int16(val)
  _x: bytes = bytes(_v)
  if sys.byteorder == 'little':
    _x = _x[::-1]
  return bytes(_x)


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

def to_uint32(val: int) -> bytes:
  """ Returns the int16 bytes for the provided value. """
  _v: c_uint16 = c_uint32(val)
  _x: bytes = bytes(_v)
  if sys.byteorder == 'little':
    _x = _x[::-1]
  return bytes(_x)


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

def to_char_bytes(_s: str) -> bytes:
  """ Returns the int16 bytes for the provided value. """
  _v: bytes = encode(_s, encoding='utf_16_be')
  return bytes(_v)


def encode_rgb(values: list[int]) -> list[float]:
    """ Returns a byte string of values for an RGB color definition.


    #### Parameters

    * values: list[float]
      * a list containing a minimum of 3 values


    #### Returns
    * bytes
      * a string of bytes containing the converted values

    """
    if (len(values) < 3):
        err: str = 'Too few values provided for RGB conversion.\n    '
        err += f'Got {len(values)}, should be at least 3.'
        raise ValueError(err)
    
    return [to_uint16(v * 256) for v in values[:3]]


def encode_hsb(values: list[float]) -> bytes:
    """ Returns a byte string of values for an HSB color definition.


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