# Mathx Tools
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

import os
import shutil
from . import FileUtils
from . import Keywords

def PrepareForCompile(fcont):
    return fcont.replace("\t", " ").split(".\n")

def RunProgram(fname):
    fname = os.path.basename(os.path.realpath(fname))
    cfname = fname[:-3] + ".c"
    cc = os.getenv("CC", "tcc")
    exe = fname[:-3]
    if os.name == 'nt':
        exe += ".exe"
    if os.system(f"{cc} {cfname} -o {exe}") != 0:
        os.remove(cfname)
        exit(-1)

def ThrowError(err):
    err.run()

def GetDataType(var):
    if var in Keywords.Vars["int"]:
        return "int"
    elif var in Keywords.Vars["double"]:
        return "double"
    elif var in Keywords.Vars["String"]:
        return "String"
    elif var in Keywords.Vars["bool"]:
        return "bool"

def GetDataTypeValue(val):
    try:
        int(val)
        return "int"
    except ValueError:
        try:
            float(val)
            return "double"
        except ValueError:
            if val == "true" or val == "false":
                return "bool"
            else:
                return "String"

def ClearTemp(tempf, fname):
    os.remove(FileUtils.cfname(tempf.name))
    tempexe = os.path.basename(os.path.realpath(tempf.name))
    tempexe = tempexe[:-3]
    fexe = os.path.basename(os.path.realpath(fname))
    fexe = fexe[:-3]
    if os.name == 'nt':
        tempexe += ".exe"
        fexe += ".exe"
    shutil.move(tempexe,fexe)