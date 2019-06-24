#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "table.h"

Table* table_open(const char* filename) {
  Pager* pager = pager_open(filename);
  Table* table = malloc(sizeof(Table));

  table->pager = pager;
  table->root_page_num = 0;

  if (pager->num_pages == 0) {
    // New database file. Initialize page 0 as leaf node.
    void* root_node = get_page(pager, 0);
    initialize_leaf_node(root_node);
    set_node_root(root_node, true);
  }
 
  return table;
}

void free_table(Table* table) {
  for (int i = 0; table->pager->pages[i]; i++) {
    free(table->pager->pages[i]);
  }
  free(table);
}

void table_flush(Table* table) {
  Pager* pager = table->pager;

  for (uint32_t i = 0; i < pager->num_pages; i++) {
    if (pager->pages[i] == NULL) {
      continue;
    }
    pager_flush(pager, i);
    free(pager->pages[i]);
    pager->pages[i] = NULL;
  }
}

void table_deallocate(Table* table) {
  Pager* pager = table->pager;

  for (uint32_t i = 0; i < TABLE_MAX_PAGES; i++) {
    void* page = pager->pages[i];
    if (page) {
      free(page);
      pager->pages[i] = NULL;
    }
  }

  free(pager);
  free(table);
}


void table_close(Table* table) {
  Pager* pager = table->pager;

  table_flush(table);

  // close the file
  int result = close(pager->file_descriptor);
  if (result == -1) {
    printf("Error closing db file.\n");
    exit(EXIT_FAILURE);
  }

  table_deallocate(table);
}
