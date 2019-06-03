#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "pager.h"

void* create_page(Pager* pager, uint32_t page_num) {
  void* page = malloc(PAGE_SIZE);
  uint32_t num_pages = pager->file_length / PAGE_SIZE;

  // We might save a partial page at the end of the file
  if (pager->file_length % PAGE_SIZE) {
    num_pages += 1;
  }

  // if we're missing some page information, read data into the page from the file
  if (page_num <= num_pages) {
    lseek(pager->file_descriptor, page_num * PAGE_SIZE, SEEK_SET);
    ssize_t bytes_read = read(pager->file_descriptor, page, PAGE_SIZE);
    if (bytes_read == -1) {
      printf("Error reading file: %d\n", errno);
      exit(EXIT_FAILURE);
    }
  }

  return page;    
}

void* get_page(Pager* pager, uint32_t page_num) {
  // if the page number is out of bounds, error & exit
  if (page_num > TABLE_MAX_PAGES) {
    printf("Tried to fetch page number out of bounds. %d > %d\n", page_num, TABLE_MAX_PAGES);
    exit(EXIT_FAILURE);
  }

  // if the requested page doesn't exist already, make one
  if (pager->pages[page_num] == NULL) {
    pager->pages[page_num] = create_page(pager, page_num);
  }

  return pager->pages[page_num];
}

Pager* pager_open(const char* filename) {
  int fd = open(
    filename,
    O_RDWR  | O_CREAT,    // Read/Write mode, create file if it does not exist
    S_IWUSR | S_IRUSR     // User write permission, or user read permission
  );

  if (fd == -1) {
    printf("Unable to open file\n");
    exit(EXIT_FAILURE);
  }

  off_t file_length = lseek(fd, 0, SEEK_END);

  Pager* pager = malloc(sizeof(Pager));
  pager->file_descriptor = fd;
  pager->file_length = file_length;

  for (uint32_t i = 0; i < TABLE_MAX_PAGES; i++) {
    pager->pages[i] = NULL;
  }

  return pager;
}

void pager_flush(Pager* pager, uint32_t page_num, uint32_t size) {
  if (pager->pages[page_num] == NULL) {
    printf("Tried to flush null page\n");
    exit(EXIT_FAILURE);
  }

  off_t offset = lseek(pager->file_descriptor, page_num * PAGE_SIZE, SEEK_SET);

  if (offset == -1) {
    printf("Error seeking: %d\n", errno);
    exit(EXIT_FAILURE);
  }

  ssize_t bytes_written =
      write(pager->file_descriptor, pager->pages[page_num], size);

  if (bytes_written == -1) {
    printf("Error writing: %d\n", errno);
    exit(EXIT_FAILURE);
  }
}
 