#ifndef CURSOR_H_
#define CURSOR_H_

#include "table.h"

struct Cursor_t {
  Table* table;
  uint32_t row_num;
  bool end_of_table; // if true, the cursor is past the position of the last element
};
typedef struct Cursor_t Cursor;

Cursor* table_start(Table* table);
Cursor* table_end(Table* table);

void* cursor_value(Cursor* cursor);
void cursor_advance(Cursor* cursor);

#endif /*CURSOR_H_*/