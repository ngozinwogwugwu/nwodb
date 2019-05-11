#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "compiler.h"

/*
 * this compiler.c file will (for now) contain functionality for:
 *  - Tokenizer
 *  - Parser
 *  - Code Generator
 */
PrepareResult prepare_statement(char* buffer, Statement* statement) {
  //  we use strncmp for "insert" since the "insert" keyword will be followed by data
  if (strncmp(buffer, "insert", strlen("insert")) == 0) {
    statement->type = STATEMENT_INSERT;
    return PREPARE_SUCCESS;
  }
  if (strcmp(buffer, "select") == 0) {
    statement->type = STATEMENT_SELECT;
    return PREPARE_SUCCESS;
  }

  return PREPARE_UNRECOGNIZED_STATEMENT;
}

void execute_statement(Statement* statement) {
  switch (statement->type) {
    case (STATEMENT_INSERT):
      printf("This is where we would do an insert.\n");
      break;
    case (STATEMENT_SELECT):
      printf("This is where we would do a select.\n");
      break;
  }
}

void handle_sql_command(char* buffer) {
  Statement statement;
  switch (prepare_statement(buffer, &statement)) {
    case (PREPARE_SUCCESS):
      break;
    case (PREPARE_UNRECOGNIZED_STATEMENT):
      printf("Unrecognized keyword at start of '%s'.\n", buffer);
      return;
  }

  execute_statement(&statement);
  printf("Executed.\n");
}
