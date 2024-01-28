from collections import defaultdict
import sys
import os
from time import sleep
from copy import copy


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")

class BFExecutor:
    def __init__(self) -> None:
        self.infArray = defaultdict(int)
        self.info = {}
        self.file_pos = [0, 0]
        self.instruction_set = []
        self.loop = []
        self.calls = []
        self.rollover_modes = [0, 8, 16, 32]
        self.arrIndex = 0
        self.rollover_mode = 0
        self.output = ""
        self.char_exception = ""
        self.debug = "debug" in sys.argv
        self.dumb = "dump" in sys.argv

    def print_debug(self, char: str) -> None:
        clear()
        print("-- BrainFunction++ Debug Process --")
        print(f"Line {self.file_pos[0] if self.file_pos[0] >= 0 else "[end]"}, Character {self.file_pos[1]}")
        print()
        print("Rollover Mode:", self.rollover_mode)
        print("Index:", self.arrIndex - 1, self.arrIndex, self.arrIndex + 1, sep="\t")
        print("Value:", self.infArray[self.arrIndex - 1], self.infArray[self.arrIndex], self.infArray[self.arrIndex + 1], sep="\t")
        print()
        print("Loop Indexes:", *self.loop, sep="\t")
        print("Func Locals:", *self.calls, sep="\t")
        print()
        print(f"Current Instruction: {self.char_exception if self.char_exception != "" else char}")
        print()
        print(f"-- Character Output --\n{self.output}")
        if "dump" in sys.argv and char == "end":
            print("\n\nDUMP:\n")
            print(dict(self.infArray))

    def exec_char(self, char: str) -> None:
        if char == "<" and self.arrIndex > 0:
            self.arrIndex -= 1
        elif char == ">":
            self.arrIndex += 1
        elif char == "+":
            self.infArray[self.arrIndex] += 1
            if self.rollover_mode != 0 and self.infArray[self.arrIndex] > 2**self.rollover_mode - 1:
                self.infArray[self.arrIndex] = 0
        elif char == "-":
            self.infArray[self.arrIndex] -= 1
            if self.rollover_mode != 0 and self.infArray[self.arrIndex] < 0:
                self.infArray[self.arrIndex] = 2**self.rollover_mode - 1
        elif char == "[":
            self.loop.append(self.file_pos[1])
        elif char == "]":
            if len(self.loop) == 0: raise f"Error: Invalid Loop at {self.arrIndex}!"
            if self.infArray[self.arrIndex] != 0:
                self.file_pos[1] = self.loop[-1]
            else:
                self.loop.pop()
        elif char == "v":
            try:
                if self.info["func"] == "call":
                    self.calls.append([self.file_pos[0], self.file_pos[1] + 1])
                    self.file_pos[0] += 1
                elif self.info["func"] == "ptr":
                    self.file_pos[0] += self.infArray[self.arrIndex]
                elif self.info["func"] == "ptrcall":
                    self.calls.append([self.file_pos[0], self.file_pos[1] + 1])
                    self.file_pos[0] += self.infArray[self.arrIndex]
                del self.info["func"]
            except:
                self.file_pos[0] += 1
            self.file_pos[1] = 0
            self.char_exception = char
            return
        elif char == "^" and self.file_pos[0] > 0:
            self.file_pos[0] -= 1
            self.file_pos[1] = 0
            self.char_exception = char
            return
        elif char == "&":
            self.info["func"] = "call"
        elif char == "*":
            self.info["func"] = "ptr"
        elif char == "$":
            self.info["func"] = "ptrcall"
        elif char == "#":
            self.rollover_mode = self.rollover_modes[(self.rollover_modes.index(self.rollover_mode) + 1) % len(self.rollover_modes)]
        elif char == ";":
            try:
                self.file_pos = self.calls.pop()
            except:
                self.file_pos[0] = -1
        
        self.char_exception = ""

    def print_char_action(self, char: str) -> None:
        if char == ",":
            i = input("Input Number: ")
            try:
                self.infArray[self.arrIndex] = int(i)
            except:
                self.infArray[self.arrIndex] = ord(i[0])
        elif char == ".":
            self.output += chr(self.infArray[self.arrIndex])
        if "debug" in sys.argv:
            if len(sys.argv) == 4: speed = 1
            else: speed = float(sys.argv[4])

            self.print_debug(char)
            sleep(speed)
    
    def interpret_line(self, line: list[str]) -> None:
        while self.file_pos[1] < len(line):
            if line[self.file_pos[1]] == '"': break

            copy_pos = copy(self.file_pos)
            self.exec_char(line[self.file_pos[1]])

            if self.file_pos[0] != copy_pos[0]:
                self.print_char_action(line[copy_pos[1]])
                return 1
            
            self.print_char_action(line[self.file_pos[1]])
            self.file_pos[1] += 1
        return 0
    
    def extract_file(self, file) -> None:
        for line in file:
            self.instruction_set.append([])
            for char in line:
                self.instruction_set[-1].append(char)

    def run_interpreter(self) -> None:
        with open(sys.argv[2]) as f:
            self.extract_file(f)

        while self.file_pos[0] < len(self.instruction_set) and self.file_pos[0] >= 0:
            if self.interpret_line(self.instruction_set[self.file_pos[0]]) == 0:
                self.file_pos[0] += 1

if __name__ == "__main__":

    if "bf++.py" in sys.argv[0]:
        sys.argv.insert(0, "py")

    if len(sys.argv) < 3:
        print()
        print("BrainFunction++, the better BF interpreter for all you programming needs.")
        print()
        print("Input Format:")
        print("\n\tpy morebf.py <file> (dump) (debug) [pausetime]")
        print("For More Information, type \"py morebf.py help\"")
        exit()
    elif len(sys.argv) == 3 and sys.argv[2] == "help":
        print()
        print("BrainFunction++ adds many things on top of Brainfuck, such as:")
        print("- A detailed debug mode")
        print("- Relative Functions")
        print("- Internal Bit Rollover Switcher")
        print("and more (coming soon)!")
        print("\tNote: For backwards compatibility for standard BF, '#' at the beginning of the program")
        print("Here's the basics:\n")
        print("\t>  - Move pointer right 1")
        print("\t<  - Move pointer left 1")
        print("\t+  - Increment Num at pointer")
        print("\t-  - Decrement Num at pointer")
        print("\t[] - Loop commands inside until num at pointer == 0")
        print("\t,  - Get a single input number/character from user")
        print("\t.  - Output a number as a Unicode character")
        print("\n-- New Stuff: --\n")
        print("\t#  - Switch Rollover Modes: None (default), 8bit, 16bit, 32bit")
        print("\tv  - Jump to line below")
        print("\t^  - Jump to line above")
        print("\t&v - Call line below")
        print("\t&^ - Call line above")
        print("\t*v - Jumps down the current memory cell's value amount of lines")
        print("\t*^ - Jumps up the current memory cell's value amount of lines")
        print("\t$v - Call down as many lines as the num at pointer")
        print("\t$^ - Call up as many lines as the num at pointer")
        print("\t;  - Call Return. MUST BE USED IF FUNCTION IS CALLED")
        print("\t\"  - Comment")
        exit()

    BF = BFExecutor()
    BF.run_interpreter()

    BF.print_debug("end")