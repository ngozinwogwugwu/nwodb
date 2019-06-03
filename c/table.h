#ifndef TABLE_H_
#define TABLE_H_

#include "pager.h"

struct Table_t {
  uint32_t num_rows;
  Pager* pager;
};
typedef struct Table_t Table;


struct Cursor_t {
  Table* table;
  uint32_t row_num;
  bool end_of_table; // if true, the cursor is past the position of the last element
};
typedef struct Cursor_t Cursor;


Table* table_open(const char* filename);
void free_table(Table* table);
void table_close(Table* table);

Cursor* table_start(Table* table);
Cursor* table_end(Table* table);

void* cursor_value(Cursor* cursor);
void cursor_advance(Cursor* cursor);

#endif /*TABLE_H_*/