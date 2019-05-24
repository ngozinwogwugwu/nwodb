# NwoDB - My attempt to build a database
I'm going off of [this tutorial](https://cstack.github.io/db_tutorial), but I'll see if I can do the same work in Python, just to make sure I understand
- [official SQLite documentation](https://cstack.github.io/db_tutorial/parts/part1.html)

# C
## Part 1: Read/Evaluate/Print Loop
writing a simple REPL (Read/Evaluate/Print Loop), according to [part 1 of the tutorial](https://cstack.github.io/db_tutorial/parts/part1.html)
- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/04c904b1331365947dcdfe6cd5ebed37af83523d)

## Part 2: Commands
My personal refactor, Implementing Meta Commands
### Refactor
The CStack DB Tutorial seems to put the entire database in [a single c file](https://github.com/cstack/db_tutorial/blob/master/db.c), so I'm going to spend some time here breaking up my code a bit. You can see the results in [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/0ed5bb1b9f2b5e05628f5599578172480578f0d3)
- I made my first Makefile
- I separated the REPL functionality into its own C file

### Meta Commands
On to the new functionality!
- Handling _meta commands_. If the first character in the input buffer is a dot, `.`, then handle that meta command. Right now, all we handle is `.exit`.
- [commit for this](https://github.com/ngozinwogwugwu/nwodb/commit/349e2c1b83ee4576c411ea5e9bb4e681e36dc8b5)

### SQL commands
- Figure out the statement type. If the statement doesn't start with a `.`, then we can expect (for now) one of two things:
  - `INSERT`
  - `SELECT`

Let's make `compiler.c`/`compiler.h` files to handle this. These files will (for now) act as the entire _SQL Compiler_ box in [SQLite's Architecture diagram](https://github.com/cstack/db_tutorial/blob/master/assets/images/arch2.gif), encompassing the Tokenizer, Parser and Code Generator.

Right now, all we need to do with it is take in a user input, attempt to prepare it (right now, that means determining the statement type) and attempt to execute it (right now, that means just printing a confirmation to the terminal)
- [commit for this](https://github.com/ngozinwogwugwu/nwodb/commit/91536e38d91229c92a79203f94f1e28cc84e02e7)

### New concepts
- **Meta-Commands**: Commands like `.exit` that start with a dot. These are as commands for the CLI, rather than SQL queries
- **Compiler**: The part of SQL that takes in a query and handles it

## Part 3: Inserts & Selects
Using [part 3 of the tuorial](https://github.com/cstack/db_tutorial/blob/master/_parts/part3.md) as a guide, we'll add limited insert/select functionality (only on memory for now). Changes:
- `vm.c`: handles the `execute_insert` and `execute_select` statements
- `backend.c`: structure definitions for table & row, serialize/deserialize row into/out of memory

More refactoring:
- rename `repl.c` to `interface.c`. Rename `compiler.c` to `sql_command_processor.c`

- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/d2b2049e20a4fefcf70067ba31724130d5c583d4)

## Part 4: Tests
Introducing [rspec](http://rspec.info), unit testing in ruby (my first ruby ever)
``` bash
sudo gem install rspec
touch test.rb
rspec test.rb
```

Things for this commit:
- catch and handle cases where the table is full
- catch and handle cases where insert strings are too long
- catch and handle cases where the insert ID is negative, or not a number
- make it possible to make inserts for strings that are _almost_ too long

Also, new unit tests. They test the following:
- inserts and retreives a row
- prints error message when table is full
- allows inserting strings that are the maximum length
- prints error message if strings are too long
- prints an error message if id is negative
- prints an error message if id is a string

- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/af142b3491aad68598f7452d278507c76f34aa7a)

## Part 5: Persistence
Okay, so in order to have persistence here, we need to write to disk. Since we're imitating SQLite, we need to make sure that we write our data in a way that matches with SQLite.
- **pager**: an abstraction that we're going to use to read/write blocks of memory. We ask for page _n_, and it gives us page _n_
  - _first it looks in the cache, then it looks on disk_
  - for now, let's keep the pager within the `backend.c`, but it would make sense to make a separate `pager.c` file later in the project

Because we're updating nwodb to save to disk, we'll be making most of our changes to `backend.c`. Specifically:
- database functions: `db_open()`, `db_close()`, `db_flush()`, `db_deallocate()`
- pager functions: `pager_flush()`, `pager_open()`, `create_page()`, `get_page()`


# Python
## Part 1
writing a simple REPL (Read/Evaluate/Print Loop), according to [part 1 of the tutorial](https://cstack.github.io/db_tutorial/parts/part1.html)
- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/13376236a74711ca51d6ac1fb6079314ba469b5a)

## Part 2
### Meta Commands
I'm separating out functionality here and making a separate REFL file. This will handle meta commands in particular
- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/8992189c91522e3b58ef4c1e56bc20caa3e74d87)

### SQL commands
In order to handle SQL commands, I'm making two new files: `compiler.py` and `sql_statement.py`. Compiler.py instantiates a SQL statement, then prepares and executes that SQL statement.

On Prepare, `SQL_statement` determines what kind of statement type we're dealing with. Right now, it can be one of two things:
  - `INSERT`
  - `SELECT`

The Execute statement just prints out what's going on for now, but we'll flesh it out later on.
- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/b733743e9379894c4d6698b16f27c394a2d026bd)

## Part 3
- add limited insert/select functionality (only on memory for now)
- update `sql_statement.py` to handle the `execute_insert` and `execute_select` statements

Tools for serialization: based on [this article](https://docs.python-guide.org/scenarios/serialization), I've decided to use Pickle Reason? Binary, native serialization. Also, I don't need to deal with importing numpy without using anaconda

- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/241f71de50d397c0a2eb80ae8b7b04e837b8c9a1)

## Part 4 - Unit Tests
I'm using the [built in python unit tests](https://docs.python.org/3/library/unittest.html) for this. Command for unittests:
```
python -m unittest test.py
```

I'm testing that my code:
- handle correct and incorrect meta commands
- handle correct and incorrect select commands
- handle correct and incorrect insert commands
- catches and handles cases where the table is full

# Tools

### Looking at byte code
If you want a good way to view a database file, you can use [hexdump](http://man7.org/linux/man-pages/man1/hexdump.1.html). When you use this on whatever database file you generate using nwodb, you should see something like this:
```bash
Ngozis-MacBook-Air:c ngozinwogwugwu$ hexdump -C my_file.db
00000000  01 00 00 00 77 6f 6e 6b  61 00 00 00 40 00 00 00  |....wonka...@...|
00000010  00 00 00 00 30 b9 2a ef  fe 7f 00 00 83 17 84 68  |....0.*........h|
00000020  ff 7f 00 00 40 77 69 6c  6c 69 65 40 77 6f 6e 6b  |....@willie@wonk|
00000030  61 2e 63 6f 6d 00 2a ef  fe 7f 00 00 98 b9 2a ef  |a.com.*.......*.|
00000040  fe 7f 00 00 00 00 00 00  00 00 00 00 20 00 00 00  |............ ...|
00000050  00 00 00 00 20 00 00 00  00 00 00 00 40 00 00 00  |.... .......@...|
```

you can specify things like output size, type of data and offset
``` bash
hexdump -d -s 16 -n 2 my_file.db
```

### Debugging in C
Over the course of this project, I discovered that [LLDB](https://lldb.llvm.org/) comes preinstalled on most macs. I also learned (over the course of a frustrating afternoon) that gdb isn't the best thing to use if you're using OS X

I got started with the help of [this tutorial](https://towardsdatascience.com/an-introduction-to-debugging-in-c-and-lldb-part-i-e3c51991f83a), and I'm keeping [this page](https://lldb.llvm.org/use/map.html#examining-variables) open while I work to use as a reference.

If you're planning on compiling your code so that it can be used with LLDB, you'll need to change the makefile slightly:
``` diff
- gcc -o nwodb nwodb.c interface.c sql_command_processor.c vm.c backend.c -I.
+ cc -g -o nwodb nwodb.c interface.c sql_command_processor.c vm.c backend.c -I.
```

Here's a list of the commands that I use the most:
``` bash

# Starts your debugger with the nwodb executable
lldb nwodb

# set a breakpoint at line 22 and run the program
breakpoint set -l 22
run

# frame var, shows variables in frame
fr v

# read from memory, specify size and format
memory read --size 1 --format char[] 0x000000010020

# execute a function, get the result
expr (int) strlen("insert")

# view a specific variable
p buffer
```
