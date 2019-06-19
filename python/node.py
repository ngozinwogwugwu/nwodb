import math
import struct
import constants
from row import Row

class Node:
  NODE_HEADER_SIZE   = 10
  NODE_HEADER_FORMAT = '<BBII'

  NODE_TYPE_INTERNAL = 0
  NODE_TYPE_LEAF     = 1

  NODE_TYPE_SIZE          =  1 # sizeof(uint8_t)
  IS_ROOT_SIZE            =  1 # sizeof(uint8_t)
  PARENT_POINTER_SIZE     =  4 # sizeof(uint32_t)
  COMMON_NODE_HEADER_SIZE = NODE_TYPE_SIZE + IS_ROOT_SIZE + PARENT_POINTER_SIZE

  LEAF_NODE_NUM_CELLS_SIZE = 4 #sizeof(uint32_t)
  LEAF_NODE_HEADER_SIZE    = COMMON_NODE_HEADER_SIZE + LEAF_NODE_NUM_CELLS_SIZE

  LEAF_NODE_KEY_SIZE   = 4 #sizeof(uint32_t)
  LEAF_NODE_VALUE_SIZE = constants.ROW_SIZE
  LEAF_NODE_CELL_SIZE  = LEAF_NODE_KEY_SIZE + LEAF_NODE_VALUE_SIZE

  LEAF_NODE_SPACE_FOR_CELLS = (constants.PAGE_SIZE - LEAF_NODE_HEADER_SIZE)
  LEAF_NODE_MAX_CELLS       = math.floor(LEAF_NODE_SPACE_FOR_CELLS / LEAF_NODE_CELL_SIZE)

  def __init__(self, page = None):
    self.type      = self.NODE_TYPE_LEAF
    self.is_root   = False
    self.parent    = 0
    self.num_cells = 0
    self.cells     = []
    self.page      = page if page else bytearray()

    if page != None: self.deserialize()


  # Use a binary search to find one of the following
  #  1. the given key
  #  2. the end of the table
  #  3. the smallest key in the node that is bigger than the given key
  def find_index(self, key):
    min_index = 0;
    max_index = self.num_cells - 1

    while max_index >= min_index:
      index = math.floor((min_index + max_index + 1)/2)
      key_at_index = self.cells[index][0]

      if key == key_at_index:
        return index
      elif key < key_at_index:
        max_index = index - 1
      else:
        min_index = index + 1

    return min_index

  def insert(self, cell_num, key, row):
    if self.num_cells > self.LEAF_NODE_MAX_CELLS:
      exit('I still need to implement leaf node splitting')

    new_cell = (key, row)

    # If we're not appending to the end of the cells, we need to insert the new cell in the middle of the group.
    # We can do that by splitting the cells array into two chunks, then inserting the new cell in the middle
    if cell_num < self.num_cells:
      self.cells = self.cells[:cell_num] + [new_cell] + self.cells[cell_num:]
    else:
      self.cells.append(new_cell)

    self.num_cells += 1
    self.serialize()
   

  def serialize(self):
    page = bytearray(
      struct.pack(constants.BOOL_FORMAT, self.type) +
      struct.pack(constants.BOOL_FORMAT, self.is_root) +
      struct.pack(constants.LITTLE_ENDIAN_INT_FORMAT, self.parent) +
      struct.pack(constants.LITTLE_ENDIAN_INT_FORMAT, self.num_cells)
    )

    for cell in self.cells:
      row = cell[1]
      row.serialize()
      page += bytearray(
        struct.pack(constants.LITTLE_ENDIAN_INT_FORMAT, cell[0]) +
        row.byte_buffer
      )

    filler = bytearray(constants.PAGE_SIZE - len(page))
    page = page + filler

    self.page = page
    return page


  def deserialize(self):
    if len(self.page) == 0: return

    page_header_bytes = self.page[:self.NODE_HEADER_SIZE]
    page_cells_bytes  = self.page[self.NODE_HEADER_SIZE:]

    page_header    = struct.unpack(self.NODE_HEADER_FORMAT, page_header_bytes)
    self.type      = page_header[0]
    self.is_root   = page_header[1]
    self.parent    = page_header[2]
    self.num_cells = page_header[3]

    cells = []
    for i in range(0, self.num_cells):
      cell_bytes = page_cells_bytes[i*self.LEAF_NODE_CELL_SIZE : (i+1)*self.LEAF_NODE_CELL_SIZE]
      cells.append(self.cell_bytes_to_cell(cell_bytes))
    self.cells = cells


  def cell_bytes_to_cell(self, cell_bytes):
    # get the key
    key = struct.unpack(constants.LITTLE_ENDIAN_INT_FORMAT, cell_bytes[:self.LEAF_NODE_KEY_SIZE])[0]

    # get the row
    row = Row()
    row.byte_buffer = cell_bytes[self.LEAF_NODE_KEY_SIZE:]
    row.deserialize()

    return (key, row)


  def get_key(self, cell_num):
    if cell_num >= self.num_cells:
      exit('tried to access a cell that doesn\'t exist')

    return self.cells[cell_num][0]


  def get_row(self, cell_num):
    if cell_num >= self.num_cells:
      exit('tried to access a cell that doesn\'t exist')

    return self.cells[cell_num][1]











