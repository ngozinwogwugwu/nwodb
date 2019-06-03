#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "vm.h"

ExecuteResult execute_insert(Row* row_to_insert, Table* table) {
  Cursor* cursor = table_end(table);
  if (table->num_rows >= TABLE_MAX_ROWS) {
    return EXECUTE_TABLE_FULL;
  }

  serialize_row(row_to_insert, cursor_value(cursor));
  table->num_rows += 1;

  free(cursor);
  return EXECUTE_SUCCESS;
}

ExecuteResult execute_select(Table* table) {
  Cursor* cursor = table_start(table);
  Row row;
  while (!(cursor->end_of_table)) {
    deserialize_row(cursor_value(cursor), &row);
    print_row(&row);
    cursor_advance(cursor);
  }
  free(cursor);

  return EXECUTE_SUCCESS;
}

