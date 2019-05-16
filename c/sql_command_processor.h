/*****************************************************************************
 *
 *                                 NwoDb
 *
 * This is the header for the compiler.
 *
\*****************************************************************************/

#ifndef COMPILER_H_
#define COMPILER_H_

#include "backend.h"

enum PrepareResult_t {
  PREPARE_SUCCESS,
  PREPARE_NEGATIVE_ID,
  PREPARE_SYNTAX_ERROR,
  PREPARE_UNRECOGNIZED_STATEMENT,
  PREPARE_STRING_TOO_LONG
};
typedef enum PrepareResult_t PrepareResult;


enum StatementType_t { STATEMENT_INSERT, STATEMENT_SELECT };
typedef enum StatementType_t StatementType;

struct Statement_t {
  StatementType type;
  Row row_to_insert;  // only used by insert statement
};
typedef struct Statement_t Statement;

void handle_sql_command(char* buffer, Table* table);
PrepareResult prepare_insert(char* buffer, Statement* statement);
PrepareResult prepare_statement(char* buffer, Statement* statement);
void print_prepare_result(PrepareResult prepare_result);
void print_prepare_error(PrepareResult prepare_result);
#endif /*COMPILER_H_*/