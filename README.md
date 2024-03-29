# BrainFunctionPlus
BrainFunction++ is an addon and fixup of BrainFunction, which is based on BrainFuck. It can do many things and is still being worked on, but is currently in a bug-free state.

### What the heck is a BrainFuck?
[BrainFuck](https://en.wikipedia.org/wiki/Brainfuck) is an esoteric programming language created by Urban Müller in 1993. It was created to be a very simple language: you are given an infinite array of zeroes and 8 commands to modify them, including very basic I/O. There are Plenty of BrainFuck interpreters, even one made in BrainFuck itself!

### So then, what is BrainFunction?
[BrainFunction](https://github.com/ryanfox/brainfunction) is an esoteric programming language created by ryanfox in 2016. It was created to simply add functions to BrainFuck. While it did technically work, some of the code caused the language to act weird and unpredictable that I'm pretty sure was not intended.

### So what is this?
This is an esoteric programming lanuage created by CreateSource in 2024. It was created with intuitiveness in mind, I hope you find it as natural as I do

##### Quick Note: This is a _score-computing interpreter_, therefore, programs that use negative indexes cannot be used.

# Commands
This is a list of commands that you can currently use in BrainFunction++

| Command     | Description |
| ----------- | ----------- |
| `>`         | Moves the pointer right 1 |
| `<`         | Moves the pointer left 1  |
| `+`         | Increment pointer cell |
| `-`         | Decrement pointer cell |
| `,`         | Take number/character input |
| `.`         | Output memory cell as a Unicode character |
| `[]`        | Loop through until the cell at the end of the loop is 0 |
| `#`         | Switch between None (default), 8bit, 16bit, and 32bit rollover modes |
| `v`         | Jump down 1 line |
| `^`         | Jump up 1 line |
| `&v`        | Call line below |
| `&^`        | Call line above |
| `*v`        | Jumps down the current memory cell's value amount of lines |
| `*^`        | Jumps up the current memory cell's value amount of lines |
| `$v`        | Calls the current memory cell's value amount of lines below |
| `$^`        | Calls the current memory cell's value amount of lines above |
| `;`         | Returns from a call. END OF LINES ARE NOT RETURNS |
| `"`         | Comment, anything after is ignored. This also applies to semicolons |

 ##### All jumps and calls reset the character position to 0

 Thank you for using BrainFunction++! If you want to check out my other projects, you can find them [here](https://abnormalhare.github.io/)
