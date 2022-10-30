""" This is the entry point to using aco_reader. It only really
contains metadata.

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
__version__ = '0.3.0'

import os
import sys
from typing import Dict, List, Optional, Union

sys.path.insert(0, os.sep.join([os.path.abspath(os.curdir), '..']))
from .reader import read_file


# Argument variables
ARGUMENTS: Dict[str, Union[str, bool]] = {
    'output_directory': '.' + os.sep,
    'input_directory': '.' + os.sep,
    'fail_quiet': False,
    'verbose': False,
    'text_only': False
}


def vprint(*values: object, sep: Optional[str] = None, end: Optional[str] = None):
    """ Prints a message to the console only if the verbose flag has
    been toggled on.

    """
    if (ARGUMENTS['verbose']):
        print(values, sep=sep, end=end)

def print_preamble() -> None:
    """ Prints the application's name and copyright information
    to the console.

    """
    print('ACO Reader v0.1.0 Color Swatch Export Tool')
    print('Copyright (c) 2022, C. Lockett\n')
    print('This software is provided "as is", without warranty of any kind,')
    print('express or implied. For more details, see the LICENSE file.\n')

def print_help() -> None:
    """ Prints the application help screen to the console. """
    print('Optional Arguments:')
    print('    -h, --help                 Show help')
    print('    -o, --out-dir=<dir>        Desired directory for output files.')
    print('    -i, --in-dir=<dir>         Directory containing target .aco files.')
    print('    -q, --quiet                Fail quietly and continue onward with processing.')
    print('    -v, --verbose              Display non-critical messages.')
    print('    -t, --text                 Export text files only.')

if __name__ == '__main__':
    print_preamble()

    # Check the passed arguments to ensure that there's not any.
    # If there's an argument, we'll process it accordingly.
    if (len(sys.argv) > 1):
        # The first check we'll do is if we find the help argument.
        # If we do, then that's the one and only thing to do.
        if ('-h' in sys.argv or '--help' in sys.argv):
            print_help()
            exit()
        for i, arg in enumerate(sys.argv[1:]):
            # -o, --out-dir=<dir>
            if (arg == '-o' or '--out-dir=' in arg):
                # Retrieve the target output directory from the argument.
                t_out_dir: str = ''
                if arg == '-o':
                    t_out_dir = sys.argv[i + 2]
                    i += 1
                else:
                    t_out_dir = arg.replace('--out-dir=', '')
                t_out_dir = os.path.abspath(t_out_dir)
                if t_out_dir[-1] != os.sep: t_out_dir += os.sep
                # Check that the target output directory exists.
                if (os.path.exists(t_out_dir)):
                    ARGUMENTS['output_directory'] = t_out_dir
                else:
                    print(f'aco_reader: unable to find specified output directory. ({t_out_dir})')
                    sys.exit(0)
            # -i, --in-dir=<dir>
            if (arg == '-i' or '--in-dir=' in arg):
                # Retrieve the target output directory from the argument.
                t_in_dir: str = ''
                if arg == '-i':
                    t_in_dir = sys.argv[i + 2]
                    i += 1
                else:
                    t_in_dir = arg.replace('--in-dir=', '')
                t_in_dir = os.path.abspath(t_in_dir)
                if t_in_dir[-1] != os.sep: t_in_dir += os.sep
                # Check that the target output directory exists.
                if (os.path.exists(t_in_dir)):
                    ARGUMENTS['input_directory'] = t_in_dir
                else:
                    print(f'aco_reader: unable to find specified input directory. ({t_in_dir})')
                    sys.exit(0)
            # -q, --quiet
            if (arg == '-q' or arg == '--quiet'):
                ARGUMENTS['fail_quiet'] = True
            # -v, --verbose
            if (arg == '-v' or arg == '--verbose'):
                ARGUMENTS['verbose'] = True
            # -(t, --text
            if (arg == '-t' or arg == '--t'):
                ARGUMENTS['text_only'] = True
    # Get a list of aco files in the input directory.
    files: list[str] = [
        f for f in os.listdir(ARGUMENTS['input_directory'])
            if os.path.isfile(ARGUMENTS['input_directory'] + f)
                and f[-3:] == 'aco'
    ]
    if (len(files) > 0):
        vprint(f'Found {len(files)} .aco files to process in input directory.')
    else:
        print('aco_reader: unable to find any .aco files in the input directory.')
        sys.exit(0)
    for _f in files:
        read_file(_f, xargs=ARGUMENTS)
 