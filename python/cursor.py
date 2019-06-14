import constants
import math
from table import Table
from node import Node
from row import Row

class Cursor:

  def __init__(self, table, table_end = False):
    root_node = Node(table.get_root_page())
    num_root_node_cells = root_node.num_cells

    self.table = table
    self.page_num = table.root_page_num
    self.cell_num = num_root_node_cells if table_end else 0
    self.end_of_table = True if table_end else (num_root_node_cells == 0)


  def get_page(self):
    return self.table.pager.get_page(self.page_num)

  def advance(self, num_node_cells):
    # let's just advance the cursor within the node for now. The table only has one node
    node = Node(self.get_page())
    self.cell_num += 1
    self.end_of_table = (self.cell_num >= num_node_cells)

