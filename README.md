# NwoDB - My attempt to build a database
I'm going off of [this tutorial](https://cstack.github.io/db_tutorial), but I'll see if I can do the same work in Python, just to make sure I understand

# C
## Part 1
- [tutorial](https://cstack.github.io/db_tutorial/parts/part1.html)
- [official SQLite documentation](https://cstack.github.io/db_tutorial/parts/part1.html)
- writing a simple REPL (Read/Evaluate/Print Loop), writing a REPL in python
- [check out the commit](https://github.com/ngozinwogwugwu/nwodb/commit/04c904b1331365947dcdfe6cd5ebed37af83523d)

## Part 2
The CStack DB Tutorial seems to put the entire database in [a single c file](https://github.com/cstack/db_tutorial/blob/master/db.c), so I'm going to spend some time here breaking up my code a bit. You can see the results in [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/0ed5bb1b9f2b5e05628f5599578172480578f0d3)
- I made my first Makefile
- I separated the REPL functionality into its own C file

On to the new functionality!
- Handling _meta commands_. If the first character in the input buffer is a dot, `.`, then handle that meta command. Right now, all we handle is `.exit`. [commit for this]((https://github.com/ngozinwogwugwu/nwodb/commit/349e2c1b83ee4576c411ea5e9bb4e681e36dc8b5))
- Figure out the statement type. If the statement doesn't start with a `.`, then we can expect an `INSERT`, or something. This means we should make an enum with statement types

### New concepts
- **Meta-Commands**: Commands like `.exit` that start with a dot. These are as commands for the CLI, rather than SQL queries


# Python
## Part 1
- [tutorial](https://cstack.github.io/db_tutorial/parts/part1.html)
- [official SQLite documentation](https://cstack.github.io/db_tutorial/parts/part1.html)
- writing a simple REPL (Read/Evaluate/Print Loop), writing a REPL in python
- [check out the commit](https://github.com/ngozinwogwugwu/nwodb/commit/04c904b1331365947dcdfe6cd5ebed37af83523d)

## Part 2
