import math
import struct
import constants

class Row:

  def __init__(self, row_id = 0, name = '', email = ''):
    self.id    = row_id # id => uint32
    self.name  = name   # name => char[33]
    self.email = email  # email => char[256]
    self.byte_buffer = bytearray()


  def serialize(self):
    self.byte_buffer = bytearray(
      struct.pack(constants.LITTLE_ENDIAN_INT_FORMAT, self.id) +
      struct.pack(constants.NAME_STRING_FORMAT, bytes(self.name, 'ascii')) +
      struct.pack(constants.EMAIL_STRING_FORMAT, bytes(self.email, 'ascii'))
    )


  def print(self):
    print((self.id, self.name, self.email))


  def deserialize(self):
    row_bytes = struct.unpack(constants.ENTIRE_ROW_FORMAT, self.byte_buffer)

    self.id = row_bytes[0]
    self.name = row_bytes[1][0 : self.get_first_non_ascii_byte(row_bytes[1])].decode('ascii')
    self.email = row_bytes[2][0 : self.get_first_non_ascii_byte(row_bytes[2])].decode('ascii')


  # get the first character that isn't ascii printable
  def get_first_non_ascii_byte(self, buf):
    for i in range(0, len(buf)):
      if (buf[i] < 32) or (buf[i] > 127):
        return i

    return len(buf)