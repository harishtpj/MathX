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
import sys
from .vars import Vars

class Compiler:
    def Fstexp(stmt):
        return stmt.split(" ")[0]
    
    def Retexp(stmt):
        return stmt.split(" ", 1)[1]
    
    def Compile(program_stmt):
        cprog = ""

        for stmt in program_stmt:
            stmt = stmt.strip()
            
            if Compiler.Fstexp(stmt) == "print": # Prints String
                cprog += f"printf({Compiler.Retexp(stmt)});\n"

            elif Compiler.Fstexp(stmt) == "println": # Prints String with newline
                cprog += f"printf({Compiler.Retexp(stmt)});\n"
                cprog += "printf(\"\\n\");\n"

            elif re.search(r"set ([$@!]\w+) to ([$@!]\w+|[\"]?\w+(\.\d+)?[\"]?)", stmt): # Sets variable value
                match = re.search(r"set ([$@!]\w+) to ([$@!]\w+|[\"]?\w+(\.\d+)?[\"]?)", stmt)
                var = match.group(1)
                val = match.group(2)
                if var[1:] in Vars:
                    if val[1:] in Vars:
                        if var[0] == '$' and var[0] == '$':
                            cprog += f"strcpy({var[1:]},{val[1:]});\n"
                        else:
                            cprog += f"{var[1:]} = {val[1:]};\n"
                    else:
                        if var[0] == '$':
                            cprog += f"strcpy({var[1:]},{val});\n"
                        else:
                            cprog += f"{var[1:]} += {val};\n"

            elif re.search(r"input to ([$@!]\w+)", stmt): # Gets user input
                match = re.search(r"input to ([$@!]\w+)", stmt)
                var = match.group(1)
                if var[1:] in Vars:
                    if var[0] == '$':
                        cprog += f"scanf(\"%[^\\n]%*c\", {var[1:]});\n"
                    elif var[0] == '@':
                        cprog += f"scanf(\"%d\", &{var[1:]});\n"
                    elif var[0] == '!':
                        cprog += f"scanf(\"%lf\", &{var[1:]});\n"

            elif Compiler.Fstexp(stmt) == "!:":  # Comments
                continue

            elif re.search(r"create variable (\w+) of type (\w+)", stmt): # Creates User-Defined Variables
                match = re.search(r"create variable (\w+) of type (\w+)", stmt)
                var = match.group(1)
                vtype = match.group(2)
                cprog += f"{vtype} {var};\n"
                Vars.append(var)

            elif re.search(r"increment ([$@!]\w+)", stmt): # Increment Variable
                match = re.search(r"increment ([$@!]\w+)", stmt)
                var = match.group(1)
                if var[1:] in Vars:
                    if var[0] == '$':
                        sys.stderr.write(f"Error: String can't be incremented\n")
                        sys.stderr.write(f"Compilation terminated\n")
                        sys.exit(-1)
                    else:
                        cprog += f"++{var[1:]};\n"

            elif re.search(r"decrement ([$@!]\w+)", stmt): # Decrement Variable
                match = re.search(r"decrement ([$@!]\w+)", stmt)
                var = match.group(1)
                if var[1:] in Vars:
                    if var[0] == '$':
                        sys.stderr.write(f"Error: String can't be decremented\n")
                        sys.stderr.write(f"Compilation terminated\n")
                        sys.exit(-1)
                    else:
                        cprog += f"--{var[1:]};\n"

            elif re.search(r"add ([@!]\w+|\d+(\.\d+)?) to ([@!]\w+)", stmt): # Addition
                match = re.search(r"add ([@!]\w+|\d+(\.\d+)?) to ([@!]\w+)", stmt)
                val = match.group(1)
                var = match.group(3)
                if var[1:] in Vars:
                    if val[1:] in Vars:
                        cprog += f"{var[1:]} += {val[1:]};\n"
                    else:
                        cprog += f"{var[1:]} += {val};\n"

            elif re.search(r"subtract ([@!]\w+|\d+(\.\d+)?) from ([@!]\w+)", stmt): # Subtraction
                match = re.search(r"subtract ([@!]\w+|\d+(\.\d+)?) from ([@!]\w+)", stmt)
                val = match.group(1)
                var = match.group(3)
                if var[1:] in Vars:
                    if val[1:] in Vars:
                        cprog += f"{var[1:]} -= {val[1:]};\n"
                    else:
                        cprog += f"{var[1:]} -= {val};\n"

            elif re.search(r"multiply ([@!]\w+|\d+(\.\d+)?) with ([@!]\w+)", stmt): # Multiplication
                match = re.search(r"multiply ([@!]\w+|\d+(\.\d+)?) with ([@!]\w+)", stmt)
                val = match.group(1)
                var = match.group(3)
                if var[1:] in Vars:
                    if val[1:] in Vars:
                        cprog += f"{var[1:]} *= {val[1:]};\n"
                    else:
                        cprog += f"{var[1:]} *= {val};\n"

            elif re.search(r"divide ([@!]\w+|\d+(\.\d+)?) into ([@!]\w+)", stmt): # Division
                match = re.search(r"divide ([@!]\w+|\d+(\.\d+)?) into ([@!]\w+)", stmt)
                val = match.group(1)
                var = match.group(3)
                if var[1:] in Vars:
                    if val[1:] in Vars:
                        cprog += f"{var[1:]} /= {val[1:]};\n"
                    else:
                        cprog += f"{var[1:]} /= {val};\n"
        
        return cprog