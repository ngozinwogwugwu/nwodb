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
  char username[COLUMN_USERNAME_SIZE];
  char email[COLUMN_EMAIL_SIZE];
};
typedef struct Row_t Row;

struct Table_t {
  uint32_t num_rows;
  void* pages[TABLE_MAX_PAGES];
};
typedef struct Table_t Table;

void* get_row_slot_address(Table* table, uint32_t row_num);

void serialize_row(Row* source, void* destination);
void deserialize_row(void* source, Row* destination);
void print_row(Row* row);

Table* new_table();
void free_table(Table* table);

#endif /*BACKEND_H_*/