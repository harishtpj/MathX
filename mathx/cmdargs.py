# Mathx Command line argument parser
# Copyright (c) 2022 Harish Kumar
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
from . import __version_str__

arg_parser = argparse.ArgumentParser(prog="mathx",
                                    description="The Mathx programming language compiler")

arg_parser.add_argument('File',
                        metavar='file',
                        type=str,
                        help="The File to compile")

arg_parser.add_argument("-l",
                        "--lang",
                        action="store",
                        type=str,
                        help="the Language to Transpile")

arg_parser.add_argument("-S",
                        "--source",
                        action="store_true",
                        help="only Compiles Mathx File to Given Language")

arg_parser.add_argument("-v",
                        "--version",
                        action="version",
                        version=__version_str__,
                        help="shows version info of Mathx compiler")