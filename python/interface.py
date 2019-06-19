import sys
import constants
from sql_statement import SQL_Statement
from table import Table
from node import Node


def get_database_table():
  if (len(sys.argv) < 2):
    exit("database name required.")

  return Table(sys.argv[1])


def handle_sql_command(sql_command, table):
  sql_statement = SQL_Statement(sql_command)
  sql_statement.execute(table)

def print_leaf_node(node):
  print(
    "type      - " + str(node.type) + "\n" +
    "is_root   - " + str(node.is_root)   + "\n" +
    "parent    - " + str(node.parent)    + "\n" +
    "num_cells - " + str(node.num_cells)
  )
  for i in range(0, node.num_cells):
    node.get_row(i).print()


def print_node_constants():
  print(
    "ROW_SIZE                  - " + str(constants.ROW_SIZE)             + "\n" +
    "COMMON_NODE_HEADER_SIZE   - " + str(Node.COMMON_NODE_HEADER_SIZE)   + "\n" + 
    "LEAF_NODE_HEADER_SIZE     - " + str(Node.LEAF_NODE_HEADER_SIZE)     + "\n" + 
    "LEAF_NODE_CELL_SIZE       - " + str(Node.LEAF_NODE_CELL_SIZE)       + "\n" + 
    "LEAF_NODE_SPACE_FOR_CELLS - " + str(Node.LEAF_NODE_SPACE_FOR_CELLS) + "\n" + 
    "LEAF_NODE_MAX_CELLS       - " + str(Node.LEAF_NODE_MAX_CELLS)
  )

def handle_meta_commands(meta_command, table):
  if (meta_command == '.exit'):
    table.flush()
    exit('bye!')

  elif (meta_command == '.constants'):
    print_node_constants()

  elif (meta_command == '.tree'):
    print_leaf_node(Node(table.pager.get_page(0)))

  else:
    print('meta command not recognized: ' + meta_command)

def handle_repl_input(user_input, table):
  if (user_input[0] == '.'):
    handle_meta_commands(user_input, table)
    return

  return user_input




def nwodb_prompt(table):
  sql_command = handle_repl_input(input('nwodb >>> '), table)
  if sql_command: handle_sql_command(sql_command, table)
