#ifndef TABLE_H_
#define TABLE_H_

#include "pager.h"

struct Table_t {
  uint32_t num_rows;
  Pager* pager;
};
typedef struct Table_t Table;

Table* table_open(const char* filename);
void free_table(Table* table);
void table_close(Table* table);

#endif /*TABLE_H_*/