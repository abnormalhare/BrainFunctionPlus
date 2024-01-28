from collections import defaultdict
import sys
import os
from time import sleep
from copy import copy

infArray = defaultdict(int)
info = {}
file_pos = [0, 0]
instruction_set = []
loop = []
calls = []
rollover_modes = [0, 8, 16, 32]
arrIndex = 0
rollover_mode = 0
output = ""
char_exception = ""

def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def print_debug(c: str) -> None:
    global infArray, arrIndex, rollover_mode
    clear()
    print("-- MoreBrainFuck Debug Process --")
    print(f"Line {file_pos[0] if file_pos[0] >= 0 else "[end]"}, Character {file_pos[1]}")
    print()
    print("Rollover Mode:", rollover_mode)
    print("Index:", arrIndex - 1, arrIndex, arrIndex + 1, sep="\t")
    print("Value:", infArray[arrIndex - 1], infArray[arrIndex], infArray[arrIndex + 1], sep="\t")
    print()
    print("Loop Indexes:", *loop, sep="\t")
    print("Func Locals:", *calls, sep="\t")
    print()
    print(f"Current Instruction: {char_exception if char_exception != "" else c}")
    print()
    print(f"-- Character Output --\n{output}")
    if "dump" in sys.argv and c == "end":
        print("\n\nDUMP:\n")
        print(dict(infArray))

def exec_char(c: str) -> int | None:
    global arrIndex, infArray, loop, char_exception, rollover_mode, file_pos

    if c == "<" and arrIndex > 0:
        arrIndex -= 1
    elif c == ">":
        arrIndex += 1
    elif c == "+":
        infArray[arrIndex] += 1
        if rollover_mode != 0 and infArray[arrIndex] > 2**rollover_mode - 1:
            infArray[arrIndex] = 0
    elif c == "-":
        infArray[arrIndex] -= 1
        if rollover_mode != 0 and infArray[arrIndex] < 0:
            infArray[arrIndex] = 2**rollover_mode - 1
    elif c == "[":
        loop.append(file_pos[1])
    elif c == "]":
        if len(loop) == 0: raise f"Error: Invalid Loop at {arrIndex}!"
        if infArray[arrIndex] != 0:
            file_pos[1] = loop[-1]
        else:
            loop.pop()
    elif c == "v":
        try:
            if info["func"] == "call":
                calls.append([file_pos[0], file_pos[1] + 1])
                file_pos[0] += 1
            elif info["func"] == "ptr":
                file_pos[0] += infArray[arrIndex]
            elif info["func"] == "ptrcall":
                calls.append([file_pos[0], file_pos[1] + 1])
                file_pos[0] += infArray[arrIndex]
            del info["func"]
        except:
            file_pos[0] += 1
        file_pos[1] = 0
        char_exception = c
        return
    elif c == "^" and file_pos[0] > 0:
        file_pos[0] -= 1
        file_pos[1] = 0
        char_exception = c
        return
    elif c == "&":
        info["func"] = "call"
    elif c == "*":
        info["func"] = "ptr"
    elif c == "$":
        info["func"] = "ptrcall"
    elif c == "#":
        rollover_mode = rollover_modes[(rollover_modes.index(rollover_mode) + 1) % len(rollover_modes)]
    elif c == ";":
        try:
            file_pos = calls.pop()
        except:
            file_pos[0] = -1
    
    char_exception = ""

def print_char_action(c: str) -> None:
    global infArray, arrIndex, output

    if c == ",":
        i = input("Input Number: ")
        try:
            infArray[arrIndex] = int(i)
        except:
            infArray[arrIndex] = ord(i[0])
    elif c == ".":
        output += chr(infArray[arrIndex])
    if "debug" in sys.argv:
        if len(sys.argv) == 4: speed = 1
        else: speed = float(sys.argv[4])

        print_debug(c)
        sleep(speed)
    
def interpret_line(line: list[str]) -> None:
    global file_pos

    while file_pos[1] < len(line):
        if line[file_pos[1]] == '"': break

        copy_pos = copy(file_pos)
        exec_char(line[file_pos[1]])

        if file_pos[0] != copy_pos[0]:
            print_char_action(line[copy_pos[1]])
            return 1
        
        print_char_action(line[file_pos[1]])
        file_pos[1] += 1
    return 0

if __name__ == "__main__":

    if "morebf.py" in sys.argv[0]:
        sys.argv.insert(0, "py")

    if len(sys.argv) < 3:
        print()
        print("MoreBrainFuck, the better BF interpreter for all you programming needs.")
        print()
        print("Input Format:")
        print("\n\tpy morebf.py <file> (debug) [pausetime]")
        print("  \tpy morebf.py <file> dump")
        print("For More Information, type \"py morebf.py help\"")
        exit()
    elif len(sys.argv) == 3 and sys.argv[2] == "help":
        print()
        print("MoreBrainFuck adds many things on top of Brainfuck, such as:")
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
        print("\t*v - Jump down as many lines as the num at pointer")
        print("\t*^ - Jump up as many lines as the num at pointer")
        print("\t$v - Call down as many lines as the num at pointer")
        print("\t$^ - Call up as many lines as the num at pointer")
        print("\t;  - Call Return. MUST BE USED IF FUNCTION IS CALLED")
        print("\t\"  - Comment")
        exit()

    with open(sys.argv[2]) as f:
        for line in f:
            instruction_set.append([])
            for char in line:
                instruction_set[-1].append(char)

    while file_pos[0] < len(instruction_set) and file_pos[0] >= 0:
        if interpret_line(instruction_set[file_pos[0]]) == 0:
            file_pos[0] += 1

    print_debug("end")