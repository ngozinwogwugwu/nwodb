import utils
import math
import constants
from pager import Pager

class Table:

  def __init__(self, filename):
    self.pager = Pager(filename)
    self.num_rows = math.floor(self.pager.file_length/constants.ROW_SIZE)


  def get_row(self, row_num):
    page = self.get_row_page(row_num)
    byte_offset = (row_num % constants.ROWS_PER_PAGE) * constants.ROW_SIZE
    row_bytes = page[byte_offset : byte_offset + constants.ROW_SIZE]
    return utils.deserialize_row(row_bytes)


  def get_row_page(self, row_num):
    page_num = math.floor(row_num/constants.ROWS_PER_PAGE)
    return self.pager.get_page(page_num)


  def insert(self, row):
    user_id = row[0]
    name = row[1]
    email = row[2]
    row_bytes = utils.serialize_row(user_id, name, email)

    new_page = self.get_row_page(self.num_rows) + row_bytes
    page_num = math.floor(self.num_rows/constants.ROWS_PER_PAGE)

    self.pager.pages[page_num] = new_page
    self.num_rows = self.num_rows + 1


  def flush(self):
    # save pages to the file
    total_pages = math.ceil(self.num_rows/constants.ROWS_PER_PAGE)
    for full_page_index in range(0, total_pages):
      self.pager.flush_page(full_page_index)

    self.pager.file.close()