import constants
import math
from table import Table
from row import Row

class Cursor:

  def __init__(self, table, table_end = False):
    self.table = table

    if table_end:
      self.row_num = self.table.num_rows
      self.end_of_table = True
    else:
      self.row_num =  0
      self.end_of_table = (self.table.num_rows == 0)

  def get_row_bytes(self):
    page = self.get_row_page()
    byte_offset = (self.row_num % constants.ROWS_PER_PAGE) * constants.ROW_SIZE
    row_bytes = page[byte_offset : byte_offset + constants.ROW_SIZE]
    return page[byte_offset : byte_offset + constants.ROW_SIZE]

  def get_row_page(self):
    page_num = math.floor(self.row_num/constants.ROWS_PER_PAGE)
    return self.table.pager.get_page(page_num)

  def advance(self):
    self.row_num += 1
    self.end_of_table = (self.row_num >= self.table.num_rows)