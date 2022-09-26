# The Mathx Compiler
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

import re
import shlex
from .. import Keywords
from ..errors.runtime_error import RuntimeError
from .. import Tools

def Preprocess(stmt):
    if " greater than " in stmt: stmt = stmt.replace("greater than", ">")
    if " lesser than " in stmt: stmt = stmt.replace("lesser than", "<")
    if " and " in stmt: stmt = stmt.replace("and", "&&")
    if " or " in stmt: stmt = stmt.replace("or", "||")
    if " not " in stmt: stmt = stmt.replace("not ", "!")
    if " equal to " in stmt: stmt = stmt.replace("equal to", "==")
    if " mod " in stmt: stmt = stmt.replace("mod", "%")
    if " equals " in stmt: stmt = stmt.replace(" equals", "=")
    if "do" in stmt: stmt = stmt.replace("do", "{")
    if "end" in stmt: stmt = stmt.replace("end", "}")
    if "else" in stmt: stmt = stmt.replace("else", "} else ")
    
    return stmt

def Fstexp(stmt):
    return stmt.split(" ")[0]

def Retexp(stmt):
    return stmt.split(" ", 1)[1]

def Compile(program_stmt):
    cprog = ""
    program_stmt = [stmt.rstrip(".\n") for stmt in program_stmt]

    for stmt in program_stmt:
        stmt = stmt.strip()
        stmtlst = []
        for word in shlex.split(stmt,posix=False):
            if word[0] == "\"" and word[-1] == "\"":
                stmtlst.append(word)
            elif word[0] == "*":
                stmtlst.append(word)
            elif word == "Integer":
                stmtlst.append("int")
            elif word == "Boolean":
                stmtlst.append("bool")
            elif word == "Double":
                stmtlst.append("double")
            elif word == "String":
                stmtlst.append("String")
            else:
                stmtlst.append(word.lower())
        stmt = Preprocess(" ".join(stmtlst))
        variables = sum(Keywords.Vars.values(), [])

        if Fstexp(stmt) == "!:":  # Comments
            continue
        
        elif Fstexp(stmt) == "print": # Prints String
            stl = []
            for w in shlex.split(Retexp(stmt), posix=False):
                if w[0] in ["@", "#", "!", "$", "*"]:
                    stl.append(w[1:])
                else:
                    stl.append(w)
            stmt = Fstexp(stmt) + " " + " ".join(stl)

            cprog += f"printf({Retexp(stmt)});\n"

        elif Fstexp(stmt) == "println": # Prints String with newline
            stl = []
            for w in shlex.split(Retexp(stmt), posix=False):
                if w[0] in ["@", "#", "!", "$", "*"]:
                    stl.append(w[1:])
                else:
                    stl.append(w)
            stmt = Fstexp(stmt) + " " + " ".join(stl)

            cprog += f"printf({Retexp(stmt)});\n"
            cprog += "printf(\"\\n\");\n"
        
        elif Fstexp(stmt) == "compute": # Computes the assignment
            stl = []
            for w in shlex.split(Retexp(stmt), posix=False):
                if w[0] in ["@", "#", "!", "$", "*"]:
                    stl.append(w[1:])
                else:
                    stl.append(w)
            stmt = Fstexp(stmt) + " " + " ".join(stl)
            cprog += f"{Retexp(stmt)};\n"

        elif re.search(r"set ([$@!#]\w+) to ([$@!#]\w+|\w+\(([$@!#\*]?\w|,| |(\".*?\"))+\)|[\"]?(\w|[ ,.!])+(\.\d+)?[\"]?)", stmt): # Sets variable value
            match = re.search(r"set ([$@!#]\w+) to ([$@!#]\w+|\w+\(([$@!#\*]?\w|,| |(\".*?\"))+\)|[\"]?(\w|[ ,.!])+(\.\d+)?[\"]?)", stmt)
            var = match.group(1)
            val = match.group(2)
            if var[1:] in variables:
                if val[1:] in variables:
                    if var[0] == '$' and val[0] == '$' and var[1:] in Keywords.Vars["String"] and val[1:] in Keywords.Vars["String"]:
                        cprog += f"strcpy({var[1:]},{val[1:]});\n"
                    elif var[0] == '@' and val[0] == '@' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} = {val[1:]};\n"
                    elif var[0] == '!' and val[0] == '!' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} = {val[1:]};\n"
                    elif var[0] == '!' and val[0] == '@' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} = {val[1:]};\n"
                    elif var[0] == '@' and val[0] == '!' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} = {val[1:]};\n"
                    elif var[0] == '#' and val[0] == '#' and var[1:] in Keywords.Vars["bool"] and val[1:] in Keywords.Vars["bool"]:
                        cprog += f"{var[1:]} = {val[1:]};\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "AssignmentError",
                            f"Can't assign {val} of type {Tools.GetDataType(val[1:])} to {var}({Tools.GetDataType(var[1:])})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
                else:
                    if var[0] == '$' and var[1:] in Keywords.Vars["String"] and Tools.GetDataTypeValue(val) == "String":
                        cprog += f"strcpy({var[1:]},{val});\n"
                    elif var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} = {val};\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} = {val};\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} = {val};\n"
                    elif var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} = {val};\n"
                    elif var[0] == '#' and var[1:] in Keywords.Vars["bool"] and Tools.GetDataTypeValue(val) == "bool":
                        cprog += f"{var[1:]} = {val};\n"
                    elif re.match(r"(\w+)\(([@#!$\*]?(\w|,| |(\".*?\"))+)\)", val):
                        match = re.search(r"(\w+)\(([@#!$\*]?(\w|,| |(\".*?\"))+)\)", val)
                        fn = match.group(1)
                        args = match.group(2)
                        stl = []
                        for w in shlex.split(args, posix=False):
                            if w[0] in ["@", "#", "!", "$", "*"]:
                                stl.append(w[1:])
                            else:
                                stl.append(w)
                        args = " ".join(stl)
                        val = f"{fn}({args})"
                        cprog += f"{var[1:]} = {val};\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "AssignmentError",
                            f"Can't assign {val} of type {Tools.GetDataTypeValue(val[1:])} to {var}({Tools.GetDataType(var[1:])})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
            else:
                Tools.ThrowError(RuntimeError(
                    "VarError",
                    f"Can't find variable {var}",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))

        elif re.search(r"input to ([$@!]\w+)", stmt): # Gets user input
            match = re.search(r"input to ([$@!]\w+)", stmt)
            var = match.group(1)
            if var[1:] in variables:
                if var[0] == '$' and var[1:] in Keywords.Vars["String"]:
                    cprog += f"scanf(\"%[^\\n]%*c\", {var[1:]});\n"
                elif var[0] == '@' and var[1:] in Keywords.Vars["int"]:
                    cprog += f"scanf(\"%d\", &{var[1:]});\n"
                elif var[0] == '!' and var[1:] in Keywords.Vars["double"]:
                    cprog += f"scanf(\"%lf\", &{var[1:]});\n"
                elif var[0] == '#' and var[1:] in Keywords.Vars["bool"]:
                    cprog += f"scanf(\"%d\", &{var[1:]});\n"
            else:
                Tools.ThrowError(RuntimeError(
                    "VarError",
                    f"Can't find variable {var}",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))

        elif re.search(r"create variable [$@!#](\w+) of type (\w+)", stmt): # Creates User-Defined Variables
            match = re.search(r"create variable [$@!#](\w+) of type (\w+)", stmt)
            var = match.group(1)
            vtype = match.group(2)
            if var in variables:
                Tools.ThrowError(RuntimeError(
                    "VarError",
                    f"Can't Reassign variable {var} which was already created",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))
            elif vtype not in Keywords.Vars.keys():
                Tools.ThrowError(RuntimeError(
                    "SyntaxError",
                    f"Unknown Data Type - {vtype}",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))
            else:
                cprog += f"{vtype} {var};\n"
                Keywords.Vars[vtype].append(var)
        
        elif re.search(r"create constant \*([A-Z0-9_]+) with value ([\"]?(\w| )+(\.\d+)?[\"]?)", stmt): # Creates User-Defined Constants
            match = re.search(r"create constant \*([A-Z0-9_]+) with value ([\"]?(\w| )+(\.\d+)?[\"]?)", stmt)
            const = match.group(1)
            constval = match.group(2)
            cprog += f"#define {const} {constval}\n"

        elif re.search(r"import (\w+)", stmt): # Imports C Libraries
            match = re.search(r"import (\w+)", stmt)
            lib = match.group(1)
            cprog += f"#include \"{lib}.h\"\n"

        elif re.search(r"increment ([$@!#]\w+)", stmt): # Increment Variable
            match = re.search(r"increment ([$@!#]\w+)", stmt)
            var = match.group(1)
            if var[1:] in variables:
                if var[0] == '$':
                    Tools.ThrowError(RuntimeError(
                        "InvalidOperationsError",
                        "String can't be incremented",
                        stmt,
                        [ps.strip() for ps in program_stmt].index(stmt)+1
                    ))
                elif var[0] == '#':
                    Tools.ThrowError(RuntimeError(
                        "InvalidOperationsError",
                        "Boolean can't be incremented",
                        stmt,
                        [ps.strip() for ps in program_stmt].index(stmt)+1
                    ))
                else:
                    cprog += f"++{var[1:]};\n"
            else:
                Tools.ThrowError(RuntimeError(
                    "VarError",
                    f"Can't find variable {var}",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))

        elif re.search(r"decrement ([$@!#]\w+)", stmt): # Decrement Variable
            match = re.search(r"decrement ([$@!#]\w+)", stmt)
            var = match.group(1)
            if var[1:] in variables:
                if var[0] == '$':
                    Tools.ThrowError(RuntimeError(
                        "InvalidOperationsError",
                        "String can't be decremented",
                        stmt,
                        [ps.strip() for ps in program_stmt].index(stmt)+1
                    ))
                elif var[0] == '#':
                    Tools.ThrowError(RuntimeError(
                        "InvalidOperationsError",
                        "Boolean can't be decremented",
                        stmt,
                        [ps.strip() for ps in program_stmt].index(stmt)+1
                    ))
                else:
                    cprog += f"--{var[1:]};\n"
            else:
                Tools.ThrowError(RuntimeError(
                    "VarError",
                    f"Can't find variable {var}",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))

        elif re.search(r"add ([$@!#]\w+|\d+(\.\d+)?) to ([$@!#]\w+)", stmt): # Addition
            match = re.search(r"add ([$@!#]\w+|\d+(\.\d+)?) to ([$@!#]\w+)", stmt)
            val = match.group(1)
            var = match.group(3)
            if var[1:] in variables:
                if val[1:] in variables:
                    if var[0] == '@' and val[0] == '@' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} += {val[1:]};\n"
                    elif var[0] == '!' and val[0] == '!' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} += {val[1:]};\n"
                    elif var[0] == '!' and val[0] == '@' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} += {val[1:]};\n"
                    elif var[0] == '@' and val[0] == '!' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} += {val[1:]};\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate + on {var}({Tools.GetDataType(var[1:])}) and {val}({Tools.GetDataType(val[1:])})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
                else:
                    if var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} += {val};\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} += {val};\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} += {val};\n"
                    elif var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} += {val};\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate + on {var}({Tools.GetDataType(var[1:])}) and {val}({Tools.GetDataTypeValue(val)})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
            else:
                Tools.ThrowError(RuntimeError(
                    "VarError",
                    f"Can't find variable {var}",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))

        elif re.search(r"subtract ([$@!#]\w+|\d+(\.\d+)?) from ([$@!#]\w+)", stmt): # Subtraction
            match = re.search(r"subtract ([$@!#]\w+|\d+(\.\d+)?) from ([$@!#]\w+)", stmt)
            val = match.group(1)
            var = match.group(3)
            if var[1:] in variables:
                if val[1:] in variables:
                    if var[0] == '@' and val[0] == '@' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} -= {val[1:]};\n"
                    elif var[0] == '!' and val[0] == '!' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} -= {val[1:]};\n"
                    elif var[0] == '!' and val[0] == '@' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} -= {val[1:]};\n"
                    elif var[0] == '@' and val[0] == '!' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} -= {val[1:]};\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate - on {var}({Tools.GetDataType(var[1:])}) and {val}({Tools.GetDataType(val[1:])})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
                else:
                    if var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} -= {val};\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} -= {val};\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} -= {val};\n"
                    elif var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} -= {val};\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate - on {var}({Tools.GetDataType(var[1:])}) and {val}({Tools.GetDataTypeValue(val)})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
            else:
                Tools.ThrowError(RuntimeError(
                    "VarError",
                    f"Can't find variable {var}",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))

        elif re.search(r"multiply ([$@!#]\w+|\d+(\.\d+)?) with ([$@!#]\w+)", stmt): # Multiplication
            match = re.search(r"multiply ([$@!#]\w+|\d+(\.\d+)?) with ([$@!#]\w+)", stmt)
            val = match.group(1)
            var = match.group(3)
            if var[1:] in variables:
                if val[1:] in variables:
                    if var[0] == '@' and val[0] == '@' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} *= {val[1:]};\n"
                    elif var[0] == '!' and val[0] == '!' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} *= {val[1:]};\n"
                    elif var[0] == '!' and val[0] == '@' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} *= {val[1:]};\n"
                    elif var[0] == '@' and val[0] == '!' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} *= {val[1:]};\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate * on {var}({Tools.GetDataType(var[1:])}) and {val}({Tools.GetDataType(val[1:])})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
                else:
                    if var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} *= {val};\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} *= {val};\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} *= {val};\n"
                    elif var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} *= {val};\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate * on {var}({Tools.GetDataType(var[1:])}) and {val}({Tools.GetDataTypeValue(val)})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
            else:
                Tools.ThrowError(RuntimeError(
                    "VarError",
                    f"Can't find variable {var}",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))

        elif re.search(r"divide ([$@!#]\w+|\d+(\.\d+)?) into ([$@!#]\w+)", stmt): # Division
            match = re.search(r"divide ([$@!#]\w+|\d+(\.\d+)?) into ([$@!#]\w+)", stmt)
            val = match.group(1)
            var = match.group(3)
            if var[1:] in variables:
                if val[1:] in variables:
                    if var[0] == '@' and val[0] == '@' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} /= {val[1:]};\n"
                    elif var[0] == '!' and val[0] == '!' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} /= {val[1:]};\n"
                    elif var[0] == '!' and val[0] == '@' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} /= {val[1:]};\n"
                    elif var[0] == '@' and val[0] == '!' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} /= {val[1:]};\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate / on {var}({Tools.GetDataType(var[1:])}) and {val}({Tools.GetDataType(val[1:])})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
                else:
                    if var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} /= {val};\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} /= {val};\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} /= {val};\n"
                    elif var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} /= {val};\n"
                    elif int(val) == 0:
                        Tools.ThrowError(RuntimeError(
                            "ZeroDivisionError",
                            f"Can't divide {var} by 0",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate / on {var}({Tools.GetDataType(var[1:])}) and {val}({Tools.GetDataTypeValue(val)})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
            else:
                Tools.ThrowError(RuntimeError(
                    "VarError",
                    f"Can't find variable {var}",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))

        elif re.search(r"square ([$@!#]\w+|\d+(\.\d+)?) to ([$@!#]\w+)", stmt): # Square
            match = re.search(r"square ([$@!#]\w+|\d+(\.\d+)?) to ([$@!#]\w+)", stmt)
            val = match.group(1)
            var = match.group(3)
            if var[1:] in variables:
                if val[1:] in variables:
                    if var[0] == '@' and val[0] == '@' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} = pow({val[1:]}, 2.0);\n"
                    elif var[0] == '!' and val[0] == '!' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} = pow({val[1:]}, 2.0);\n"
                    elif var[0] == '!' and val[0] == '@' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} = pow({val[1:]}, 2.0);\n"
                    elif var[0] == '@' and val[0] == '!' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} = pow({val[1:]}, 2.0);\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate ^2 on {val}({Tools.GetDataType(val[1:])})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
                else:
                    if var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} = pow({val}, 2.0);\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} = pow({val}, 2.0);\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} = pow({val}, 2.0);\n"
                    elif var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} = pow({val}, 2.0);\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate ^2 on {val}({Tools.GetDataTypeValue(val)})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
            else:
                Tools.ThrowError(RuntimeError(
                    "VarError",
                    f"Can't find variable {var}",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))

        elif re.search(r"sqrt ([$@!#]\w+|\d+(\.\d+)?) to ([$@!#]\w+)", stmt): # Square root
            match = re.search(r"sqrt ([$@!#]\w+|\d+(\.\d+)?) to ([$@!#]\w+)", stmt)
            val = match.group(1)
            var = match.group(3)
            if var[1:] in variables:
                if val[1:] in variables:
                    if var[0] == '@' and val[0] == '@' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} = sqrt({val[1:]});\n"
                    elif var[0] == '!' and val[0] == '!' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} = sqrt({val[1:]});\n"
                    elif var[0] == '!' and val[0] == '@' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} = sqrt({val[1:]});\n"
                    elif var[0] == '@' and val[0] == '!' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} = sqrt({val[1:]});\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate ^1/2 on {val}({Tools.GetDataType(val[1:])})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
                else:
                    if var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} = sqrt({val});\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} = sqrt({val});\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} = sqrt({val});\n"
                    elif var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} = sqrt({val});\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate ^1/2 on {val}({Tools.GetDataType(val[1:])})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
            else:
                Tools.ThrowError(RuntimeError(
                    "VarError",
                    f"Can't find variable {var}",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))
        
        elif re.search(r"cube ([$@!#]\w+|\d+(\.\d+)?) to ([$@!#]\w+)", stmt): # Cube
            match = re.search(r"cube ([$@!#]\w+|\d+(\.\d+)?) to ([$@!#]\w+)", stmt)
            val = match.group(1)
            var = match.group(3)
            if var[1:] in variables:
                if val[1:] in variables:
                    if var[0] == '@' and val[0] == '@' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} = pow({val[1:]}, 3.0);\n"
                    elif var[0] == '!' and val[0] == '!' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} = pow({val[1:]}, 3.0);\n"
                    elif var[0] == '!' and val[0] == '@' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} = pow({val[1:]}, 3.0);\n"
                    elif var[0] == '@' and val[0] == '!' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} = pow({val[1:]}, 3.0);\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate ^3 on {val}({Tools.GetDataType(val[1:])})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
                else:
                    if var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} = pow({val}, 3.0);\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} = pow({val}, 3.0);\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} = pow({val}, 3.0);\n"
                    elif var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} = pow({val}, 3.0);\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate ^3 on {val}({Tools.GetDataType(val[1:])})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
            else:
                Tools.ThrowError(RuntimeError(
                    "VarError",
                    f"Can't find variable {var}",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))
        
        elif re.search(r"cbrt ([$@!#]\w+|\d+(\.\d+)?) to ([$@!#]\w+)", stmt): # Cube root
            match = re.search(r"cbrt ([$@!#]\w+|\d+(\.\d+)?) to ([$@!#]\w+)", stmt)
            val = match.group(1)
            var = match.group(3)
            if var[1:] in variables:
                if val[1:] in variables:
                    if var[0] == '@' and val[0] == '@' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} = pow({val[1:]}, ceil((1/3.0)*100)/100);\n"
                    elif var[0] == '!' and val[0] == '!' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} = pow({val[1:]}, ceil((1/3.0)*100)/100);\n"
                    elif var[0] == '!' and val[0] == '@' and var[1:] in Keywords.Vars["double"] and val[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} = pow({val[1:]}, ceil((1/3.0)*100)/100);\n"
                    elif var[0] == '@' and val[0] == '!' and var[1:] in Keywords.Vars["int"] and val[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} = pow({val[1:]}, ceil((1/3.0)*100)/100);\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate ^1/3 on {var}({Tools.GetDataType(var[1:])}) and {val}({Tools.GetDataType(val[1:])})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
                else:
                    if var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} = pow({val}, ceil((1/3.0)*100)/100);\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} = pow({val}, ceil((1/3.0)*100)/100);\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(val) == "int":
                        cprog += f"{var[1:]} = pow({val}, ceil((1/3.0)*100)/100);\n"
                    elif var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(val) == "double":
                        cprog += f"{var[1:]} = pow({val}, ceil((1/3.0)*100)/100);\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate ^1/3 on {var}({Tools.GetDataType(var[1:])}) and {val}({Tools.GetDataTypeValue(val)})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
            else:
                Tools.ThrowError(RuntimeError(
                    "VarError",
                    f"Can't find variable {var}",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))

        elif re.search(r"power ([$@!#]\w+) with ([$@!#]\w+|\d+(\.\d+)?)", stmt): # Power var with exp
            match = re.search(r"power ([$@!#]\w+) with ([$@!#]\w+|\d+(\.\d+)?)", stmt)
            exp = match.group(2)
            var = match.group(1)
            if var[1:] in variables:
                if exp[1:] in variables:
                    if var[0] == '@' and exp[0] == '@' and var[1:] in Keywords.Vars["int"] and exp[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} = pow({var[1:]}, {exp[1:]});\n"
                    elif var[0] == '!' and exp[0] == '!' and var[1:] in Keywords.Vars["double"] and exp[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} = pow({var[1:]}, {exp[1:]});\n"
                    elif var[0] == '!' and exp[0] == '@' and var[1:] in Keywords.Vars["double"] and exp[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} = pow({var[1:]}, {exp[1:]});\n"
                    elif var[0] == '@' and exp[0] == '!' and var[1:] in Keywords.Vars["int"] and exp[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} = pow({var[1:]}, {exp[1:]});\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate ^{exp[1:]} on {var}({Tools.GetDataType(var[1:])})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
                else:
                    if var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(exp) == "int":
                        cprog += f"{var[1:]} = pow({var[1:]}, {exp});\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(exp) == "double":
                        cprog += f"{var[1:]} = pow({var[1:]}, {exp});\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(exp) == "int":
                        cprog += f"{var[1:]} = pow({var[1:]}, {exp});\n"
                    elif var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(exp) == "double":
                        cprog += f"{var[1:]} = pow({var[1:]}, {exp});\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate ^{exp} on {var}({Tools.GetDataType(var[1:])})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
            else:
                Tools.ThrowError(RuntimeError(
                    "VarError",
                    f"Can't find variable {var}",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))
        
        elif re.search(r"root ([$@!#]\w+) with ([$@!#]\w+|\d+(\.\d+)?)", stmt): # root var with exp
            match = re.search(r"root ([$@!#]\w+) with ([$@!#]\w+|\d+(\.\d+)?)", stmt)
            exp = match.group(2)
            var = match.group(1)
            if var[1:] in variables:
                if exp[1:] in variables:
                    if var[0] == '@' and exp[0] == '@' and var[1:] in Keywords.Vars["int"] and exp[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} = pow({var[1:]}, ceil((1.0/{exp[1:]})*100)/100);\n"
                    elif var[0] == '!' and exp[0] == '!' and var[1:] in Keywords.Vars["double"] and exp[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} = pow({var[1:]}, ceil((1.0/{exp[1:]})*100)/100);\n"
                    elif var[0] == '!' and exp[0] == '@' and var[1:] in Keywords.Vars["double"] and exp[1:] in Keywords.Vars["int"]:
                        cprog += f"{var[1:]} = pow({var[1:]}, ceil((1.0/{exp[1:]})*100)/100);\n"
                    elif var[0] == '@' and exp[0] == '!' and var[1:] in Keywords.Vars["int"] and exp[1:] in Keywords.Vars["double"]:
                        cprog += f"{var[1:]} = pow({var[1:]}, ceil((1.0/{exp[1:]})*100)/100);\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate ^{exp[1:]} on {var}({Tools.GetDataType(var[1:])})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
                else:
                    if var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(exp) == "int":
                        cprog += f"{var[1:]} = pow({var[1:]}, ceil((1.0/{exp})*100)/100);\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(exp) == "double":
                        cprog += f"{var[1:]} = pow({var[1:]}, ceil((1.0/{exp})*100)/100);\n"
                    elif var[0] == '!' and var[1:] in Keywords.Vars["double"] and Tools.GetDataTypeValue(exp) == "int":
                        cprog += f"{var[1:]} = pow({var[1:]}, ceil((1.0/{exp})*100)/100);\n"
                    elif var[0] == '@' and var[1:] in Keywords.Vars["int"] and Tools.GetDataTypeValue(exp) == "double":
                        cprog += f"{var[1:]} = pow({var[1:]}, ceil((1.0/{exp})*100)/100);\n"
                    else:
                        Tools.ThrowError(RuntimeError(
                            "InvalidOperationsError",
                            f"Can't operate ^{exp} on {var}({Tools.GetDataType(var[1:])})",
                            stmt,
                            [ps.strip() for ps in program_stmt].index(stmt)+1
                        ))
            else:
                Tools.ThrowError(RuntimeError(
                    "VarError",
                    f"Can't find variable {var}",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))
        
        elif re.search(r"if (.*) then", stmt): #If Condition
            match = re.search(r"if (.*) then", stmt)
            ifcond = match.group(1)
            cprog += f"if ({ifcond})" + "{\n"
        
        elif re.search(r"(\w+)\(([@#!$\*]?(\w|,| |(\".*?\"))+)\)", stmt): # Function Syntax
            match = re.search(r"(\w+)\(([@#!$\*]?(\w|,| |(\".*?\"))+)\)", stmt)
            fn = match.group(1)
            args = match.group(2)
            stl = []
            for w in shlex.split(args, posix=False):
                if w[0] in ["@", "#", "!", "$", "*"]:
                    stl.append(w[1:])
                else:
                    stl.append(w)
            args = " ".join(stl)
            cprog += f"{fn}({args});\n"
        
        else:
            if stmt == '':
                continue
            else:
                Tools.ThrowError(RuntimeError(
                    "SyntaxError",
                    "Invalid Statement",
                    stmt,
                    [ps.strip() for ps in program_stmt].index(stmt)+1
                ))
            
    
    return cprog