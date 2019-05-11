# NwoDB - My attempt to build a database
I'm going off of [this tutorial](https://cstack.github.io/db_tutorial), but I'll see if I can do the same work in Python, just to make sure I understand
- [official SQLite documentation](https://cstack.github.io/db_tutorial/parts/part1.html)

# C
## Part 1
writing a simple REPL (Read/Evaluate/Print Loop), according to [part 1 of the tutorial](https://cstack.github.io/db_tutorial/parts/part1.html)
- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/04c904b1331365947dcdfe6cd5ebed37af83523d)

## Part 2
My personal refactor, Implementing Meta Commands
### Refactor
The CStack DB Tutorial seems to put the entire database in [a single c file](https://github.com/cstack/db_tutorial/blob/master/db.c), so I'm going to spend some time here breaking up my code a bit. You can see the results in [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/0ed5bb1b9f2b5e05628f5599578172480578f0d3)
- I made my first Makefile
- I separated the REPL functionality into its own C file

### Meta Commands
On to the new functionality!
- Handling _meta commands_. If the first character in the input buffer is a dot, `.`, then handle that meta command. Right now, all we handle is `.exit`. [commit for this]((https://github.com/ngozinwogwugwu/nwodb/commit/349e2c1b83ee4576c411ea5e9bb4e681e36dc8b5))

### SQL commands
- Figure out the statement type. If the statement doesn't start with a `.`, then we can expect (for now) one of two things:
  - `INSERT`
  - `SELECT`

Let's make `compiler.c`/`compiler.h` files to handle this. These files will (for now) act as the entire _SQL Compiler_ box in [SQLite's Architecture diagram](https://github.com/cstack/db_tutorial/blob/master/assets/images/arch2.gif), encompassing the Tokenizer, Parser and Code Generator.

Right now, all we need to do with it is take in a user input, attempt to prepare it (right now, that means determining the statement type) and attempt to execute it (right now, that means just printing a confirmation to the terminal)


### New concepts
- **Meta-Commands**: Commands like `.exit` that start with a dot. These are as commands for the CLI, rather than SQL queries


# Python
## Part 1
writing a simple REPL (Read/Evaluate/Print Loop), according to [part 1 of the tutorial](https://cstack.github.io/db_tutorial/parts/part1.html)
- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/04c904b1331365947dcdfe6cd5ebed37af83523d)

## Part 2
### Meta Commands
I'm separating out functionality here and making a separate REFL file. This will handle meta commands in particular
- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/8992189c91522e3b58ef4c1e56bc20caa3e74d87)
