import math
import constants
from pager import Pager

class Table:

  def __init__(self, filename):
    self.pager = Pager(filename)
    self.root_page_num = 0

  def get_page(self, page_num):
    return self.pager.get_page(page_num)

  def get_root_page(self):
    return self.get_page(self.root_page_num)

  # save pages to the file
  def flush(self):
    total_pages = 1
    for page_num in range(0, total_pages):
      self.pager.flush_page(page_num)

    self.pager.file.close()