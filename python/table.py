import math
import constants
from pager import Pager

class Table:

  def __init__(self, filename):
    self.pager = Pager(filename)
    self.num_rows = math.floor(self.pager.file_length/constants.ROW_SIZE)

  def flush(self):
    # save pages to the file
    total_pages = math.ceil(self.num_rows/constants.ROWS_PER_PAGE)
    for full_page_index in range(0, total_pages):
      self.pager.flush_page(full_page_index)

    self.pager.file.close()