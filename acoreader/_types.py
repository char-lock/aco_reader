""" This contains all classes utilised by ACOReader. """
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


from enum import Enum
from typing import Dict, List, TypedDict


class ColorSpace(Enum):
    """ An Adobe swatch color space """
    RGB = 0
    HSB = 1
    CMYK = 2
    PANTONE = 3     # Custom color space; undecodable.
    FOCOLTONE = 4   # Custom color space; undecodable.
    TRUMATCH = 5    # Custom color space; undecodable.
    TOYO88 = 6      # Custom color space; undecodable.
    LAB = 7
    GRAYSCALE = 8
    HKS = 10        # Custom color space; undecodable.
    UNSET = -1
    
    @classmethod
    def from_value(self, value: int) -> 'ColorSpace':
        if value == 0:
            return ColorSpace.RGB
        elif value == 1:
            return ColorSpace.HSB
        elif value == 2:
            return ColorSpace.CMYK
        elif value == 3:
            return ColorSpace.PANTONE
        elif value == 4:
            return ColorSpace.FOCOLTONE
        elif value == 5:
            return ColorSpace.TRUMATCH
        elif value == 6:
            return ColorSpace.TOYO88
        elif value == 7:
            return ColorSpace.LAB
        elif value == 8:
            return ColorSpace.GRAYSCALE
        elif value == 10:
            return ColorSpace.HKS
        else:
            return ColorSpace.UNSET


def validate_color_space(color_space: ColorSpace) -> None:
    """ Checks the given color space and raises a ValueError if there
    is any issue with it.
    
    """
    if color_space.value in [-1, 3, 4, 5, 6, 10]:
        err: str = f'The selected color value ({color_space.name}) has '
        err += 'not been handled as of yet.'
        raise ValueError(err)
        
class ColorSpaceLimit(TypedDict):
    _max: float
    _min: float

COLOR_SPACE_LIMITS: Dict[ColorSpace, List[ColorSpaceLimit]] = {
    ColorSpace.RGB: [
        ColorSpaceLimit(_max = 255.00, _min = 0.00),
        ColorSpaceLimit(_max = 255.00, _min = 0.00),
        ColorSpaceLimit(_max = 255.00, _min = 0.00)
    ],
    ColorSpace.HSB: [
        ColorSpaceLimit(_max = 100.00, _min = 0.00),
        ColorSpaceLimit(_max = 100.00, _min = 0.00),
        ColorSpaceLimit(_max = 100.00, _min = 0.00)
    ],
    ColorSpace.CMYK: [
        ColorSpaceLimit(_max = 100.00, _min = 0.00),
        ColorSpaceLimit(_max = 100.00, _min = 0.00),
        ColorSpaceLimit(_max = 100.00, _min = 0.00),
        ColorSpaceLimit(_max = 100.00, _min = 0.00)
    ],
    ColorSpace.LAB: [
        ColorSpaceLimit(_max = 100.00, _min = 0.00),
        ColorSpaceLimit(_max = 127.00, _min = -128.00),
        ColorSpaceLimit(_max = 127.00, _min = -128.00)
    ],
    ColorSpace.GRAYSCALE: [
        ColorSpaceLimit(_max = 100.00, _min = 0.00)
    ]
}

COLOR_SPACE_LABELS: Dict[ColorSpace, List[str]] = {
    ColorSpace.RGB: ['RED', 'GREEN', 'BLUE'],
    ColorSpace.HSB: ['HUE', 'SATURATION', 'BRIGHTNESS'],
    ColorSpace.CMYK: ['CYAN', 'MAGENTA', 'YELLOW', 'BLACK'],
    ColorSpace.LAB: ['LIGHTNESS', 'CHROMINANCE_A', 'CHROMINANCE_B'],
    ColorSpace.GRAYSCALE: ['BRIGHTNESS']
}

class ColorSwatch(object):
    """ An object representing an Adobe ACO color swatch. """
    def __init__(self, name: str, color_space: ColorSpace, values: List[float]):
        """ A constructor for a new ColorSwatch. """
        self._color_space: ColorSpace = None
        self._color_values: Dict[str, float] = None
        self.name: str = name
        self.color_space = color_space
        self.color_values = values

    def __str__(self) -> str:
        _str: List[str] = [
            'ColorSwatch {\n',
            f'    name: \'{self.name}\',\n',
            f'    color_space: {self.color_space.name},\n',
             '    values: {\n',
        ]
        for k in self.color_values.keys():
            _str.append(f'        {k.lower()} = {self.color_values[k]:.2f},\n')
        _str.append('    }\n')
        _str.append('}\n\n')
        return ''.join(_str)

    @property
    def color_space(self) -> ColorSpace:
        """ The color space for this color swatch. """
        if self._color_space is None:
            return ColorSpace.UNSET
        return self._color_space
    
    @color_space.setter
    def color_space(self, color_space: ColorSpace):
        """ Sets the color space for the swatch. Note that this will
        raise a ValueError if an unimplemented color space is chosen
        or if the color space is already set.

        """
        validate_color_space(color_space)
        if self.color_space is ColorSpace.UNSET:
            self._color_space = color_space
        else:
            err: str = 'The color space for this swatch has already'
            err += ' been set.'
            raise ValueError(err)            
    
    @property
    def color_values(self) -> Dict[str, float]:
        """ A list containing the swatch's color values. """
        return self._color_values
    
    @color_values.setter
    def color_values(self, values: List[float]):
        if self.color_space not in COLOR_SPACE_LIMITS.keys():
            err: str = 'Unable to validate values as the color space'
            err += ' has not been set.'
            raise ValueError(err)
        else:
            for i, v in enumerate(values):
                _under: bool = v < COLOR_SPACE_LIMITS[self.color_space][i]['_min']
                _over: bool = v > COLOR_SPACE_LIMITS[self.color_space][i]['_max']
                if _under or _over:
                    err: str = f'Value {i} is outside of the value'
                    err += ' limits for {self.color_space.name}.'
                    raise ValueError(err)
            value_labels: List[str] = COLOR_SPACE_LABELS[self.color_space]
            if len(value_labels) != len(values):
                err: str = 'Provided values does not match the amount '
                err += 'of values required by the color space.\n'
                err += f'    values = {len(values)}; '
                err += f'need = {len(value_labels)}'
                raise ValueError(err)
            cv: Dict[str, float] = {}
            for i in range(len(value_labels)):
                cv[value_labels[i]] = values[i]
            self._color_values = cv
