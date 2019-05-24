/*****************************************************************************
 *
 *                                 NwoDb
 *
 * This is the header for the NwoDb API.
 *
 * The NwoDb API comprises a set of functions that allows client software
 * to access and manipulate NwoDb files, including executing SQL statements
 * on them.
 *
\*****************************************************************************/

#ifndef BACKEND_H_
#define BACKEND_H_

#define COLUMN_USERNAME_SIZE 32
#define COLUMN_EMAIL_SIZE 255
#define TABLE_MAX_PAGES 100

const uint32_t ID_SIZE;
const uint32_t USERNAME_SIZE;
const uint32_t EMAIL_SIZE;
const uint32_t ID_OFFSET;
const uint32_t USERNAME_OFFSET;
const uint32_t EMAIL_OFFSET;
const uint32_t ROW_SIZE;
const uint32_t PAGE_SIZE;
const uint32_t ROWS_PER_PAGE;
const uint32_t TABLE_MAX_ROWS;

#define size_of_attribute(Struct, Attribute) sizeof(((Struct*)0)->Attribute);

struct Row_t {
  uint32_t id;
  char username[COLUMN_USERNAME_SIZE + 1];
  char email[COLUMN_EMAIL_SIZE + 1];
};
typedef struct Row_t Row;

struct Pager_t {
  int file_descriptor;
  uint32_t file_length;
  void* pages[TABLE_MAX_PAGES];
};
typedef struct Pager_t Pager;

struct Table_t {
  uint32_t num_rows;
  Pager* pager;
};
typedef struct Table_t Table;

void* get_row_slot_address(Table* table, uint32_t row_num);

void serialize_row(Row* source, void* destination);
void deserialize_row(void* source, Row* destination);
void print_row(Row* row);

Table* db_open(const char* filename);
void free_table(Table* table);
void* create_page(Pager* pager, uint32_t page_num);
void* get_page(Pager* pager, uint32_t page_num);
Pager* pager_open(const char* filename);
void db_close(Table* table);
void pager_flush(Pager* pager, uint32_t page_num, uint32_t size);

#endif /*BACKEND_H_*/