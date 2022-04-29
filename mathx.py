# MAthX - Max of Maths
# Mathx is a compiled programming language which Transpiles itself to C

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


# Python Imports
import os
import tempfile


# Compiler Imports
from mathx.Cmdargs import arg_parser
from mathx import FileUtils
from mathx import Tools
from mathx.c import Compiler

class Mathx:
    @staticmethod
    def Run(fname, lang):
        program_stmt = FileUtils.ReadFileAsLines(fname)

        if lang == "java":
            pass
        else:
            mainfunc = Compiler.Compile(program_stmt)

        tempf = tempfile.NamedTemporaryFile()
        FileUtils.WriteCProgram(tempf.name, mainfunc)
        Tools.RunProgram(tempf.name)
        Tools.ClearTemp(tempf, fname)
    
    @staticmethod
    def Compile(fname, lang):
        program_stmt = FileUtils.ReadFileAsLines(fname)

        if lang == "java":
            pass
        else:
            mainfunc = Compiler.Compile(program_stmt)

        FileUtils.WriteCProgram(fname, mainfunc)

    @staticmethod
    def Main():
        args = arg_parser.parse_args()
        if args.source:
            Mathx.Compile(args.File, args.lang)
        else:
            Mathx.Run(args.File, args.lang)


Mathx.Main()