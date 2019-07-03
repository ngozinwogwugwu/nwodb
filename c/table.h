#ifndef TABLE_H_
#define TABLE_H_

#include "pager.h"

struct Table_t {
  uint32_t root_page_num;
  Pager* pager;
};
typedef struct Table_t Table;

Table* table_open(const char* filename);
void free_table(Table* table);
void table_close(Table* table);
void create_new_root(Table* table, uint32_t right_child_page_num);
void * create_new_leaf_node(Table* table);

#endif /*TABLE_H_*/