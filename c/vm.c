#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "vm.h"
#include "backend.h"

ExecuteResult execute_insert(Row* row_to_insert, Table* table) {
  if (table->num_rows >= TABLE_MAX_ROWS) {
    return EXECUTE_TABLE_FULL;
  }

  serialize_row(row_to_insert, get_row_slot_address(table, table->num_rows));
  table->num_rows += 1;

  return EXECUTE_SUCCESS;
}

ExecuteResult execute_select(Table* table) {
  Row row;
  for (uint32_t i = 0; i < table->num_rows; i++) {
    deserialize_row(get_row_slot_address(table, i), &row);
    print_row(&row);
  }
  return EXECUTE_SUCCESS;
}

