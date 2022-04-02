# Mathx File Utilities
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

import sys
import os

from .template import cprogram


class FileUtils:
    @staticmethod
    def isFile(fname):
        if not os.path.exists(fname):
            sys.stderr.write(f"Error: Cannot open file {fname}\n")
            sys.stderr.write(f"Compilation terminated\n")
            sys.exit(-1)

    @staticmethod
    def ReadFile(fname):
        FileUtils.isFile(fname)
        fcont = ""
        with open(fname) as fr:
            fcont = fr.read()
        if fcont[-1] != '\n':
            sys.stderr.write(f"Error: {fname} should end with a newline\n")
            sys.stderr.write(f"Compilation terminated\n")
            sys.exit(-1)
        return fcont
    
    @staticmethod
    def WriteFile(fname, fcont):
        with open(fname, "w") as fr:
            fr.write(fcont)

    @staticmethod
    def WriteCProgram(fname, prog):
        fname = os.path.basename(os.path.realpath(fname))
        cfname = fname[:-3] + ".c"
        cprog = cprogram + prog + "return 0;\n}"
        FileUtils.WriteFile(cfname, cprog)
        