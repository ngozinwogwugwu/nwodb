#ifndef PAGER_H_
#define PAGER_H_

#include <stdint.h>
#include "row.h"

#define PAGE_SIZE       (4096) // 4 kilobytes
#define TABLE_MAX_PAGES (100)
#define ROWS_PER_PAGE   (PAGE_SIZE / 293) // PAGE_SIZE /  ROW_SIZE
#define TABLE_MAX_ROWS  (ROWS_PER_PAGE * TABLE_MAX_PAGES) // PAGE_SIZE / 293

struct Pager_t {
  int file_descriptor;
  uint32_t file_length;
  void* pages[TABLE_MAX_PAGES];
};
typedef struct Pager_t Pager;

void* create_page(Pager* pager, uint32_t page_num);
void* get_page(Pager* pager, uint32_t page_num);
Pager* pager_open(const char* filename);
void pager_flush(Pager* pager, uint32_t page_num, uint32_t size);


#endif /*PAGER_H_*/