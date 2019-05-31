import constants
import struct

# id => uint32
# name => char[33]
# email => char[256]
def serialize_row(user_id, name, email):
  buf = bytearray(
    struct.pack(constants.LITTLE_ENDIAN_INT_FORMAT, user_id) +
    struct.pack(constants.NAME_STRING_FORMAT, bytes(name, 'ascii')) +
    struct.pack(constants.EMAIL_STRING_FORMAT, bytes(email, 'ascii'))
  )
  return buf


def deserialize_row(buf):
  row_bytes = struct.unpack(constants.ENTIRE_ROW_FORMAT, buf)

  user_id = row_bytes[0]
  name = row_bytes[1][0 : get_first_non_ascii_byte(row_bytes[1])].decode('ascii')
  email = row_bytes[2][0 : get_first_non_ascii_byte(row_bytes[2])].decode('ascii')

  return (user_id, name, email)

# get the first character that isn't ascii printable
def get_first_non_ascii_byte(buf):
  for i in range(0, len(buf)):
    if (buf[i] < 32) or (buf[i] > 127):
      return i

  return len(buf)