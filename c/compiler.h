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

#ifndef COMPILER_H_
#define COMPILER_H_

enum PrepareResult_t { PREPARE_SUCCESS, PREPARE_UNRECOGNIZED_STATEMENT };
typedef enum PrepareResult_t PrepareResult;

enum StatementType_t { STATEMENT_INSERT, STATEMENT_SELECT };
typedef enum StatementType_t StatementType;

struct Statement_t {
  StatementType type;
};
typedef struct Statement_t Statement;

PrepareResult prepare_statement(char* buffer, Statement* statement);
void handle_sql_command(char* buffer);
void execute_statement(Statement* statement);

#endif /*COMPILER_H_*/