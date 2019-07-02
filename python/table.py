import math
import constants
from pager import Pager
from leaf_node import Leaf_Node

class Table:

  def __init__(self, filename):
    self.pager = Pager(filename)
    self.root_page_num = 0

    # If this is a new database file: initialize the root node
    if self.pager.num_pages == 0:
      root_node = Leaf_Node(self.pager.get_page(self.root_page_num))
      root_node.is_root = True
      self.pager.insert_new_page(root_node)


  def get_page(self, page_num):
    return self.pager.get_page(page_num)

  def get_root_page(self):
    return self.get_page(self.root_page_num)

  # save pages to the file
  def flush(self):
    for page_num in range(0, self.pager.num_pages):
      self.pager.flush_page(page_num)

    self.pager.file.close()

