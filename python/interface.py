import sys
import constants
from sql_statement import SQL_Statement
from table import Table
from node import Node
from leaf_node import Leaf_Node
from internal_node import Internal_Node


def get_database_table():
  if (len(sys.argv) < 2):
    exit("database name required.")

  return Table(sys.argv[1])


def handle_sql_command(sql_command, table):
  sql_statement = SQL_Statement(sql_command)
  sql_statement.execute(table)

def print_leaf_node(leaf_node):
  for i in range(0, leaf_node.num_cells):
    leaf_node.get_row(i).print()


def print_node_constants():
  print(
    "ROW_SIZE                  - " + str(constants.ROW_SIZE)             + "\n" +
    "COMMON_NODE_HEADER_SIZE   - " + str(Leaf_Node.COMMON_NODE_HEADER_SIZE)   + "\n" + 
    "LEAF_NODE_HEADER_SIZE     - " + str(Leaf_Node.LEAF_NODE_HEADER_SIZE)     + "\n" + 
    "LEAF_NODE_CELL_SIZE       - " + str(Leaf_Node.LEAF_NODE_CELL_SIZE)       + "\n" + 
    "LEAF_NODE_SPACE_FOR_CELLS - " + str(Leaf_Node.LEAF_NODE_SPACE_FOR_CELLS) + "\n" + 
    "LEAF_NODE_MAX_CELLS       - " + str(Leaf_Node.LEAF_NODE_MAX_CELLS)
  )

def print_tree(table):
  root_node = Internal_Node(table.pager.get_page(table.root_page_num))
  if root_node.type == Node.NODE_TYPE_LEAF:
    print_leaf_node(Leaf_Node(table.pager.get_page(0)))
    return;

  print("num keys: " + str(root_node.num_cells))
  for key in range(0, root_node.num_cells):
    (page_num, max_key) = root_node.cells[key]
    print_leaf_node(Leaf_Node(table.pager.get_page(page_num)))
    print("max key: " + str(max_key))

  right_child_node = Leaf_Node(table.pager.get_page(root_node.right_child))
  print_leaf_node(right_child_node)


def handle_meta_commands(meta_command, table):
  if (meta_command == '.exit'):
    table.flush()
    exit('bye!')

  elif (meta_command == '.constants'):
    print_node_constants()

  elif (meta_command == '.btree'):
    print_tree(table)

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
