import math
import constants
from table         import Table
from row           import Row
from cursor        import Cursor
from leaf_node     import Leaf_Node
from internal_node import Internal_Node
from node          import Node

class VM:
  def insert_row(self, row, table):
    # set up the cursor and the leaf node
    key_to_insert = row.id
    cursor = Cursor(table)
    cursor.find_page(key_to_insert)
    leaf_node = Leaf_Node(cursor.get_page())
    cursor.set_cell_num(leaf_node, key_to_insert)

    # do some checks. If the table is full or that row is already occupied, return an error
    if cursor.cell_num < leaf_node.num_cells and leaf_node.get_key(cursor.cell_num) == key_to_insert:
      print("Error: Duplicate key.")
      return

    if leaf_node.num_cells >= Leaf_Node.LEAF_NODE_MAX_CELLS:
      root_node = self.split_nodes_and_insert_row(leaf_node, (key_to_insert, row), cursor.cell_num, table)
      table.pager.overwrite_page(root_node, cursor.page_num)
      return

    # update the leaf node, then update the table
    leaf_node.insert(cursor.cell_num, key_to_insert, row)
    table.pager.overwrite_page(leaf_node, cursor.page_num)


  def select_all_rows(self, table):
    cursor = Cursor(table)
    leaf_node = Leaf_Node(table.get_page(cursor.page_num))

    while cursor.end_of_table == False:
      leaf_node.get_row(cursor.cell_num).print()
      cursor.advance(leaf_node.num_cells)


  def split_nodes_and_insert_row(self, old_leaf_node, cell, cell_num, table):
    (left_leaf_node, right_leaf_node) = self.make_right_and_left_leaf_nodes(old_leaf_node.cells, cell, cell_num)

    if old_leaf_node.is_root:
      return self.create_root_node(left_leaf_node, right_leaf_node, table)

    else:
      exit("Need to implement updating parent after split")

  def make_right_and_left_leaf_nodes(self, node_cells, new_cell, cell_num):
    # create an array that includes the cell to insert
    if cell_num < (len(node_cells)):
      node_cells = node_cells[:cell_num] + [new_cell] + node_cells[cell_num:]
    else:
      node_cells.append(new_cell)

    # split the array into left and right
    left_cells = node_cells[:Leaf_Node.LEAF_NODE_LEFT_SPLIT_COUNT]
    right_cells = node_cells[Leaf_Node.LEAF_NODE_RIGHT_SPLIT_COUNT:]

    return (self.new_leaf_node(left_cells), self.new_leaf_node(right_cells))


  def new_leaf_node(self, cells):
    leaf_node = Leaf_Node()
    leaf_node.cells = cells
    leaf_node.num_cells = len(cells)
    return leaf_node


  def create_root_node(self, left_child_node, right_child_node, table):
    root = Internal_Node()
    root.is_root = True

    right_page_num = table.pager.insert_new_page(right_child_node)
    root.right_child = right_page_num

    left_page_num = table.pager.insert_new_page(left_child_node)
    left_node_max_key = left_child_node.get_max_key()
    root.set_child(left_page_num, left_node_max_key)

    return root

