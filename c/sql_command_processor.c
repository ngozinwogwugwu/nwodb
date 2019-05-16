#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sql_command_processor.h"
#include "backend.h"
#include "vm.h"

PrepareResult prepare_statement(char* buffer, Statement* statement) {
  //  we use strncmp for "insert" since the "insert" keyword will be followed by data
  if (strncmp(buffer, "insert", strlen("insert")) == 0) {
    return prepare_insert(buffer, statement);
  }
  if (strcmp(buffer, "select") == 0) {
    statement->type = STATEMENT_SELECT;
    return PREPARE_SUCCESS;
  }

  return PREPARE_UNRECOGNIZED_STATEMENT;
}



PrepareResult prepare_insert(char* buffer, Statement* statement) {
  statement->type = STATEMENT_INSERT;

  char* keyword = strtok(buffer, " ");
  char* id_string = strtok(NULL, " ");
  char* username = strtok(NULL, " ");
  char* email = strtok(NULL, " ");

  if (id_string == NULL || username == NULL || email == NULL) {
    return PREPARE_SYNTAX_ERROR;
  }

  int id = atoi(id_string);
  if (id <= 0) {
    return PREPARE_NEGATIVE_ID;
  }
  if (strlen(username) > COLUMN_USERNAME_SIZE) {
    return PREPARE_STRING_TOO_LONG;
  }
  if (strlen(email) > COLUMN_EMAIL_SIZE) {
    return PREPARE_STRING_TOO_LONG;
  }

  statement->row_to_insert.id = id;
  strcpy(statement->row_to_insert.username, username);
  strcpy(statement->row_to_insert.email, email);

  return PREPARE_SUCCESS;
}

void handle_prepare_result(PrepareResult prepare_result) {
  switch(prepare_result) {
    case (PREPARE_SYNTAX_ERROR):
      printf("Error: Syntax Error\n");
      break;
    case (PREPARE_UNRECOGNIZED_STATEMENT):
      printf("Error: Unrecognized statement.\n");
      break;
    case (PREPARE_STRING_TOO_LONG):
      printf("Error: String is too long.\n");
      break;
    case (PREPARE_NEGATIVE_ID):
      printf("Error: ID must be a positive integer.\n");
      break;
    case (PREPARE_SUCCESS):
      // do nothing
      break;
  }
}

void handle_execute_result(ExecuteResult execute_result) {
  switch(execute_result) {
    case (EXECUTE_SUCCESS):
      printf("executed\n");
      break;
    case (EXECUTE_TABLE_FULL):
      printf("Error: Table full.\n");
      break;
  }
}

ExecuteResult execute_statement(Statement* statement, Table* table) {
  switch (statement->type) {
    case (STATEMENT_INSERT):
      return execute_insert(&(statement->row_to_insert), table);
      break;
    case (STATEMENT_SELECT):
      return execute_select(table);
      break;
  }
}

void handle_sql_command(char* buffer, Table* table) {
  Statement statement;

  PrepareResult prepare_result = prepare_statement(buffer, &statement);
  handle_prepare_result(prepare_result);
  if (prepare_result != PREPARE_SUCCESS) return;

  ExecuteResult execute_result = execute_statement(&statement, table);
  handle_execute_result(execute_result);

}
