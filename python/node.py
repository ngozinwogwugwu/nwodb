import struct
import math
import constants

class Node:
  NODE_HEADER_SIZE   = 10
  NODE_HEADER_FORMAT = '<BBII'

  NODE_TYPE_INTERNAL = 0
  NODE_TYPE_LEAF     = 1

  NODE_TYPE_SIZE          =  1 # sizeof(uint8_t)
  IS_ROOT_SIZE            =  1 # sizeof(uint8_t)
  PARENT_POINTER_SIZE     =  4 # sizeof(uint32_t)
  COMMON_NODE_HEADER_SIZE = NODE_TYPE_SIZE + IS_ROOT_SIZE + PARENT_POINTER_SIZE

  def __init__(self, page = None):
    self.type      = self.NODE_TYPE_LEAF
    self.is_root   = False
    self.parent    = 0
    self.num_cells = 0
    self.cells     = []
    self.page      = page if page else bytearray()
    
    if self.page != None: self.deserialize()

  # Use a binary search to find one of the following
  #  1. the given key
  #  2. the end of the table
  #  3. the smallest key in the node that is bigger than the given key
  def find_index(self, key):
    min_index = 0;
    max_index = self.num_cells - 1

    while max_index >= min_index:
      index = math.floor((min_index + max_index + 1)/2)
      key_at_index = self.get_key(index)

      if key == key_at_index:
        return index
      elif key < key_at_index:
        max_index = index - 1
      else:
        min_index = index + 1

    return min_index

  def get_key(self, cell_num):
    (key, value) = self.get_cell(cell_num)

    # the values for internal nodes are the cell numbers
    if self.type == self.NODE_TYPE_INTERNAL:
      return value

    return key

  def get_max_key(self):
    # get the key from the final cell in the cells array
    return self.get_key(-1)

  def get_cell_value(self, cell_num):
    (key, value) = self.get_cell(cell_num)
    return value

  def get_cell(self, cell_num):
    if cell_num >= self.num_cells:
      exit('tried to access a cell that doesn\'t exist')

    return self.cells[cell_num]


  def deserialize(self):
    if len(self.page) == 0: return
    page_header_bytes = self.page[:self.NODE_HEADER_SIZE]

    page_header    = struct.unpack(self.NODE_HEADER_FORMAT, page_header_bytes)
    self.type      = page_header[0]
    self.is_root   = page_header[1]
    self.parent    = page_header[2]
    self.num_cells = page_header[3]
    self.cells     = []

