import math

BOOL_FORMAT              = 'B'
LITTLE_ENDIAN_INT_FORMAT = '<I'

# field sizes
ID_FIELD_SIZE    = 4
NAME_FIELD_SIZE  = 33
EMAIL_FIELD_SIZE = 256
ROW_SIZE         = ID_FIELD_SIZE + NAME_FIELD_SIZE + EMAIL_FIELD_SIZE # 293 bytes

# table/page information
TABLE_MAX_PAGES = 100
PAGE_SIZE       = 4096 # 4 kilobytes
ROWS_PER_PAGE   = math.floor(PAGE_SIZE/ROW_SIZE)  # 13 rows per page
TABLE_MAX_ROWS  = ROWS_PER_PAGE * TABLE_MAX_PAGES

