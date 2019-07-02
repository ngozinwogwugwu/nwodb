import struct
import constants
import math

from node import Node

class Internal_Node(Node):
  # Internal Node Header Layout
  INTERNAL_NODE_NUM_KEYS_SIZE      = 4 #sizeof(uint32_t)
  INTERNAL_NODE_RIGHT_CHILD_SIZE   = 4 #sizeof(uint32_t)
  INTERNAL_NODE_HEADER_SIZE        = Node.COMMON_NODE_HEADER_SIZE + INTERNAL_NODE_NUM_KEYS_SIZE + INTERNAL_NODE_RIGHT_CHILD_SIZE
  INTERNAL_NODE_HEADER_FORMAT      = '<BBIII'

  # Internal Node Body Layout: Cells
  INTERNAL_NODE_KEY_SIZE   = 4 #sizeof(uint32_t)
  INTERNAL_NODE_CHILD_SIZE = 4 #sizeof(uint32_t)
  INTERNAL_NODE_CELL_SIZE  = INTERNAL_NODE_CHILD_SIZE + INTERNAL_NODE_KEY_SIZE

  def __init__(self, page = None):
    super(Internal_Node, self).__init__(page)

    self.type        = Node.NODE_TYPE_INTERNAL
    self.num_keys    = 0
    self.right_child = 0

    if self.page != None: self.deserialize()

  def get_child(self, child_num):
    return super(Leaf_Node, self).get_cell_value(child_num)

  def set_child(self, page_num, node_max_key):
    self.cells.append((page_num, node_max_key))
    self.num_keys += 1

  def serialize(self):
    # internal node header (14 bytes)
    page = bytearray(
      struct.pack(constants.BOOL_FORMAT, self.type) +
      struct.pack(constants.BOOL_FORMAT, self.is_root) +
      struct.pack(constants.LITTLE_ENDIAN_INT_FORMAT, self.parent) +
      struct.pack(constants.LITTLE_ENDIAN_INT_FORMAT, self.num_keys) +
      struct.pack(constants.LITTLE_ENDIAN_INT_FORMAT, self.right_child)
    )

    for cell in self.cells:
      (page_num, max_key) = cell
      page += bytearray(
        struct.pack(constants.LITTLE_ENDIAN_INT_FORMAT, page_num) +
        struct.pack(constants.LITTLE_ENDIAN_INT_FORMAT, max_key)
      )

    filler = bytearray(constants.PAGE_SIZE - len(page))
    page = page + filler

    self.page = page
    return page

  def deserialize(self):
    if len(self.page) == 0: return
    page_header_bytes = self.page[:self.INTERNAL_NODE_HEADER_SIZE]

    page_header      = struct.unpack(self.INTERNAL_NODE_HEADER_FORMAT, page_header_bytes)
    self.type        = page_header[0]
    self.is_root     = page_header[1]
    self.parent      = page_header[2]
    self.num_keys    = page_header[3]
    self.right_child = page_header[4]
    cells = []

    page_cells_bytes  = self.page[self.INTERNAL_NODE_HEADER_SIZE:]
    for i in range(0, self.num_keys):
      cell_bytes = page_cells_bytes[i*self.INTERNAL_NODE_CELL_SIZE : (i+1)*self.INTERNAL_NODE_CELL_SIZE]
      cells.append(self.cell_bytes_to_cell(cell_bytes))
    self.cells = cells

  def cell_bytes_to_cell(self, cell_bytes):
    # get the child node page num
    page_num = struct.unpack(constants.LITTLE_ENDIAN_INT_FORMAT, cell_bytes[:self.INTERNAL_NODE_KEY_SIZE])[0]
    
    # get the child node max key
    max_key = struct.unpack(constants.LITTLE_ENDIAN_INT_FORMAT, cell_bytes[self.INTERNAL_NODE_KEY_SIZE:])[0]
    
    return (page_num, max_key)




