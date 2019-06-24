#ifndef PAGER_H_
#define PAGER_H_

#include <stdint.h>
#include "node.h"

#define PAGE_SIZE       (4096) // 4 kilobytes
#define TABLE_MAX_PAGES (100)

struct Pager_t {
  int      file_descriptor;
  uint32_t file_length;
  int32_t  num_pages;
  void*    pages[TABLE_MAX_PAGES]; // what's up with this?
};
typedef struct Pager_t Pager;

void* create_page(Pager* pager, uint32_t page_num);
void* get_page(Pager* pager, uint32_t page_num);
Pager* pager_open(const char* filename);
void pager_flush(Pager* pager, uint32_t page_num);
uint32_t get_unused_page_num(Pager* pager);

#endif /*PAGER_H_*/