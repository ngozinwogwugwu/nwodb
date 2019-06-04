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

#ifndef VM_H_
#define VM_H_

#include "cursor.h"

enum ExecuteResult_t { EXECUTE_SUCCESS, EXECUTE_TABLE_FULL };
typedef enum ExecuteResult_t ExecuteResult;

ExecuteResult execute_insert(Row* row_to_insert, Table* table);
ExecuteResult execute_select(Table* table);

#endif /*VM_H_*/