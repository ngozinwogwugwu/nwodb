import struct
import constants
import math

from row  import Row
from node import Node

class Leaf_Node(Node):
  # header layout
  LEAF_NODE_NUM_CELLS_SIZE = 4 #sizeof(uint32_t)
  LEAF_NODE_HEADER_SIZE    = Node.COMMON_NODE_HEADER_SIZE + LEAF_NODE_NUM_CELLS_SIZE

  # cell layout
  LEAF_NODE_KEY_SIZE   = 4 #sizeof(uint32_t)
  LEAF_NODE_VALUE_SIZE = constants.ROW_SIZE
  LEAF_NODE_CELL_SIZE  = LEAF_NODE_KEY_SIZE + LEAF_NODE_VALUE_SIZE

  # total layout
  LEAF_NODE_SPACE_FOR_CELLS = (constants.PAGE_SIZE - LEAF_NODE_HEADER_SIZE)
  LEAF_NODE_MAX_CELLS       = math.floor(LEAF_NODE_SPACE_FOR_CELLS / LEAF_NODE_CELL_SIZE)

  # split information
  LEAF_NODE_RIGHT_SPLIT_COUNT = math.floor((LEAF_NODE_MAX_CELLS + 1) / 2)
  LEAF_NODE_LEFT_SPLIT_COUNT  = (LEAF_NODE_MAX_CELLS + 1) - LEAF_NODE_RIGHT_SPLIT_COUNT

  def __init__(self, page = None):
    super(Leaf_Node, self).__init__(page)

    self.type = Node.NODE_TYPE_LEAF
    if self.page != None: self.deserialize()

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

  def get_row(self, cell_num):
    return super(Leaf_Node, self).get_cell_value(cell_num)

  def serialize(self):
    # leaf node header (10 bytes)
    page = bytearray(
      struct.pack(constants.BOOL_FORMAT, self.type) +
      struct.pack(constants.BOOL_FORMAT, self.is_root) +
      struct.pack(constants.LITTLE_ENDIAN_INT_FORMAT, self.parent) +
      struct.pack(constants.LITTLE_ENDIAN_INT_FORMAT, self.num_cells)
    )

    for cell in self.cells:
      (key, row) = cell
      row = row
      row.serialize()
      page += bytearray(
        struct.pack(constants.LITTLE_ENDIAN_INT_FORMAT, key) +
        row.byte_buffer
      )

    filler = bytearray(constants.PAGE_SIZE - len(page))
    page = page + filler

    self.page = page
    return page


  def deserialize(self):
    super(Leaf_Node, self).deserialize()
    page_cells_bytes  = self.page[self.NODE_HEADER_SIZE:]
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
