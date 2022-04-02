# Maths Command line argument parser

import argparse
from . import __version_str__

arg_parser = argparse.ArgumentParser(prog="mathx",
                                    description="The Mathx programming language compiler")

arg_parser.add_argument('File',
                        metavar='file',
                        type=str,
                        help="The File to compile")

arg_parser.add_argument("-v",
                        "--version",
                        action="version",
                        version=__version_str__,
                        help="shows version info of Mathx compiler")