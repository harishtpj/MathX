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

class Compiler:
    def Fstexp(stmt):
        return stmt.split(" ")[0]
    
    def Retexp(stmt):
        return stmt.split(" ", 1)[1]
    
    def Compile(program_stmt):
        cprog = ""

        for stmt in program_stmt:
            if Compiler.Fstexp(stmt) == "print":
                cprog += f"printf({Compiler.Retexp(stmt)});\n"
            elif Compiler.Fstexp(stmt) == "println":
                cprog += f"printf({Compiler.Retexp(stmt)});\n"
                cprog += "printf(\"\\n\");\n"
            elif re.search(r"set ([$@!]\w+) to ([\"]?\w+[\"]?)", stmt):
                match = re.search(r"set ([$@!]\w+) to ([\"]?\w+[\"]?)", stmt)
                var = match.group(1)
                val = match.group(2)
                if var[0] == '$':
                    cprog += f"strcpy({var[1:]},{val});\n"
                else:
                    cprog += f"{var[1:]} = {val};\n"
            elif re.search(r"input to ([$@!]\w+)", stmt):
                match = re.search(r"input to ([$@!]\w+)", stmt)
                var = match.group(1)
                if var[0] == '$':
                    cprog += f"scanf(\"%[^\\n]%*c\", {var[1:]});\n"
                elif var[0] == '@':
                    cprog += f"scanf(\"%d\", &{var[1:]});\n"
                elif var[0] == '!':
                    cprog += f"scanf(\"%lf\", &{var[1:]});\n"
        
        return cprog