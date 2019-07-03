<a href='http://www.recurse.com' title='Made with love at the Recurse Center'><img src='https://cloud.githubusercontent.com/assets/2883345/11325206/336ea5f4-9150-11e5-9e90-d86ad31993d8.png' height='20px'/></a>

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
- `table.c`: structure definitions for table & row, serialize/deserialize row into/out of memory

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
  - for now, let's keep the pager within the `table.c`, but it would make sense to make a separate `pager.c` file later in the project

Because we're updating nwodb to save to disk, we'll be making most of our changes to `table.c`. Specifically:
- database functions: `table_open()`, `table_close()`, `table_flush()`, `table_deallocate()`
- pager functions: `pager_flush()`, `pager_open()`, `create_page()`, `get_page()`

- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/35ad2da8ed0abe792bb4974a176dc4c2a9284785)

## Part 6: The Cursor
A cursor represents a location in the table. We can "move it around" the table by updating its `row_num` attribute

Before I start, I think it's time to refactor:
- split `backend.c` up into `pager.c`, `row.c` and `table.c`

After that, add `cursor` to `table.c` and update the `execute` and `select` functions to use it.

- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/93307104ea4fccf8f05946bfb0904e883fffb0c0)
- [another commit](https://github.com/ngozinwogwugwu/nwodb/commit/b37d82a813437f305a6c0fb34e494eea76ae85b2) (moving the cursor functionality into its own file)

## Part 8: Implementing a Leaf Node
So instead of saving rows directly to the table, we're goning to save them to a node. Each node has a header. The header saves the following information
- `node_type` - whether it's a leaf node or an internal node. For now, we're only making leaf nodes
- `is_root` - whether it's the root of the tree. For now, we're only dealing with a single node, so we can ignore this field
- `pointer_to_parent` - this is also something we can ignore for now
- `num_cells` - the number of cells in the node. Each cell contains a `key` and a `value `. In this case, the `value` is the row that we're inserting

Since we're inserting into the node, we need to update the cursor. Rather than pointing directly to a row, We need to update the cursor so that it points at the **node** within the table, and the **cell** within the node

We need to update the `pager`. We're going to think of pages as nodes here, so the only difference we need to make with the pager is for it to keep track of `num_pages`, rather than `file_length`

We're making some updates to the table, too. We instantiate tables with a `root_page_number` (not something we need to think too hard about right now) instead of `num_rows`. If no leaf node exists, we need to make a new one. We need to update the `table_flush` function so that it flushes full pages, no partial ones.

- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/69ac2c3bbf4cb2935b2c250f97f34934546b57e1)

## Part 9: Binary Search and Duplicate Keys
We're going to update this database so that it inserts your rows in order. This means that it can't have any duplicate keys, and it'll reject those. The changes we need to make are in `node.c`, `cursor.c` and `vm.c`

### Changes to node.c
- add a getter and a setter for the `node_type`. This means we can set it when we initialize the node, and we can get it later on when we want to check that the type of the node we're inserting to is indeed a leaf node.
- `leaf_node_find_index()`: given a node and key, find the index that we'll use to insert the row

### Changes to cursor.c
- replace `table_end()` with `table_find()`. `table_find()` returns a cursor that is pointing at the cell closest to the given key, rather than the end of the table

### Changes to vm.c
- update `execute_insert()` to make sure there aren't duplicate keys, and to use `table_find()` rather than `table_end()`

## Part 10: Splitting A Leaf Node
We're going to split a leaf node when it gets too big for a page to hold. This means that when a node has enough entries to exceed four KB, we need to do the following:
1. allocate another page (this will represent the right leaf node)
2. copy the biggest values to the right leaf node
3. Turn the original page into an internal node:
  a. allocate another page for the left node, copy all the smaller values to that page
  b. overwrite the data on the original node. Set the type to be an internal node, and indicate which pages are its left and right nodes

This means we have to flesh out our idea of an internal node and update our VM so that it can handle the leaf node split

- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/47d3a9c27a21824c86f7403a6d184cde5d2ea464)


## Part 11: Recursively Searching the B-Tree
Okay, so we're basically just adding `internal_node_find()`. This function does a binary search on the internal node in order to find the page number of its child. Once it does that, we can pull up that leaf node and use `leaf_node_find()` to find the row.

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

- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/c44bd02070b1419712dac7e8bc78f50e4f667c2c)

## Part 5 - Persistence
We need a way to make things persist. Also we need to figure out this pager stuff

### Pagers
**pages** are just blocks of data. In our case, we're using four kilobytes, but it can be whatever size you want. We're going to use a **pager** to load, store, and save all of our table data
- the user doesn't really see the pager work, it's where we store the data and it doubles as a cache
- the pager writes to disk when we're done with the program

### table
The table is what we use to look up the data based on row. We give it the row number, and it grabs that row information from its pager


### serialization
I switched from `pickle` to `struct.pack` here. [the struct library](https://docs.python.org/3/library/struct.html) is good for storing things
- to serialize, the biggest trick is to find the right format. `struct.pack` returns a byte object, and we can combine all the outputs into a byte array
- to deserialize, there's a gotchya: if there's any garbage data, python will complain. That's why I include the function `get_first_non_ascii_byte()`, so that we can limit our deserialization for the *name* and *email*

- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/4c1402337e1b98faae31439b161f07d2ae63f900)

## Part 6 - Cursor
First of all, I'm going to refactor again. Let's create a separate `Row` class. This will handle everything we were dealing with in `utils` (serialize/deserialize/print row), so we can also get rid of the `utils` file.

Now let's add a `cursor` class. The cursor is a bookmark, and we use it to keep track of where we are for inserts and selects. This means that we can move a lot of the functionality from the `table` class to the `cursor` class (like `get_row` and `get_row_page`)


## Part 8 - Implementing a Leaf Node
So instead of saving rows directly to the table, we're goning to save them to a node. Each node has a header. The header saves the following information
- `node_type` - whether it's a leaf node or an internal node. For now, we're only making leaf nodes
- `is_root` - whether it's the root of the tree. For now, we're only dealing with a single node, so we can ignore this field
- `pointer_to_parent` - this is also something we can ignore for now
- `num_cells` - the number of cells in the node. Each cell contains a `key` and a `value `. In this case, the `value` is the row that we're inserting

Since we're inserting into the node, we need to update the cursor. Rather than pointing directly to a row, We need to update the cursor so that it points at the **node** within the table, and the **cell** within the node

We need to update the `pager`. We're going to think of pages as nodes here, so the only difference we need to make with the pager is for it to keep track of `num_pages`, rather than `file_length`

We're making some updates to the table, too. We instantiate tables with a `root_page_number` (not something we need to think too hard about right now) instead of `num_rows`. If no leaf node exists, we need to make a new one. We need to update the `table_flush` function so that it flushes full pages, no partial ones.

- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/16d80611fb0410d8db7afd536c0407ad3c1e1565)

## Part 9 - Binary Search and Duplicate Keys
We need to update the database so it does two things:
1. insert rows so that they're stored in order of key
2. prevent users from entering rows with duplicate keys

The first change we need to make is to `node.py`. We need to implement a `find_index()` function, that takes a _key_ and returns an _index_. The interesting thing about the `find_index()` function is that it uses _binary search_ to determine the index. We also update the constructor so that it sets the `type` to be `NODE_TYPE_LEAF`

After that, we update `cursor.py` with a `set_cell_num()` function. This function takes a key, and uses `node.find_index()` to set the `cell_num`. We use this cursor to inform `sql_statement.py` about where exactly to insert. If there's already a cell there that has that key, report an error to the user.

## Part 10 - Splitting a Leaf Node
So the first thing we need is a concept of an internal node. This is basically the same as a Leaf node, but the header contains a pointer to the right child, and the cells are all (highest-keys/nth-child). Most of the work here is going to be creating a generic node class, and using it as the base for a leaf node class and and internal node class.

After that, we need to handle actual splits. I'm doing the splits in a new class called `VM.py` (since it was starting to get ridiculous to handle everything in the SQL_Statement class). I essentially create a new left and right node using the values in the original node (along with the user-inserted value). After that, I create a new internal node to serve as the root, and I used it to replace the initial leaf node.

- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/3702fb1d5da9950f2ca89a109cb9f0c7143a5b53)

The last step was to make sure I was splitting the leaf node correctly. This means:
- A. Unit tests
- B. A way to print out the tree

- [the commit](https://github.com/ngozinwogwugwu/nwodb/commit/186006a0704c3eeaa4f95c7b62e855f9548138db)

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
- gcc -o nwodb nwodb.c interface.c sql_command_processor.c vm.c table.c -I.
+ cc -g -o nwodb nwodb.c interface.c sql_command_processor.c vm.c table.c -I.
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
