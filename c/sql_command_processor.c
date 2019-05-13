#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sql_command_processor.h"
#include "backend.h"
#include "vm.h"

void print_prepare_result(PrepareResult prepare_result) {
  switch (prepare_result) {
    case (PREPARE_SUCCESS):
      printf("PREPARE_SUCCESS\n");
      break;
    case (PREPARE_SYNTAX_ERROR):
      printf("PREPARE_SYNTAX_ERROR\n");
      break;
    case (PREPARE_UNRECOGNIZED_STATEMENT):
      printf("PREPARE_UNRECOGNIZED_STATEMENT\n");
      break;
  }
}

PrepareResult prepare_statement(char* buffer, Statement* statement) {
  //  we use strncmp for "insert" since the "insert" keyword will be followed by data
  if (strncmp(buffer, "insert", strlen("insert")) == 0) {
    statement->type = STATEMENT_INSERT;
    int args_assigned = sscanf(
      buffer,
      "insert %d %s %s",
      &(statement->row_to_insert.id),
      statement->row_to_insert.username,
      statement->row_to_insert.email
    );
    if (args_assigned < 3) {
      return PREPARE_SYNTAX_ERROR;
    }
    return PREPARE_SUCCESS;
  }
  if (strcmp(buffer, "select") == 0) {
    statement->type = STATEMENT_SELECT;
    return PREPARE_SUCCESS;
  }

  return PREPARE_UNRECOGNIZED_STATEMENT;
}

ExecuteResult execute_statement(Statement* statement, Table* table) {
  switch (statement->type) {
    case (STATEMENT_INSERT):
      printf("STATEMENT_INSERT\n");
      return execute_insert(&(statement->row_to_insert), table);
      break;
    case (STATEMENT_SELECT):
      printf("STATEMENT_SELECT\n");
      return execute_select(table);
      break;
  }
}

void handle_sql_command(char* buffer, Table* table) {
  Statement statement;

  PrepareResult prepare_result = prepare_statement(buffer, &statement);
  print_prepare_result(prepare_result);

  if (prepare_result == PREPARE_SUCCESS) {
    ExecuteResult execute_result = execute_statement(&statement, table);
  }
}
