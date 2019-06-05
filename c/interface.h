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

#ifndef REPL_H_
#define REPL_H_

#include "table.h"

struct InputBuffer_t {
  char* buffer;
  size_t buffer_length;
  ssize_t input_length;
};
typedef struct InputBuffer_t InputBuffer;

enum MetaCommandResult_t {
  META_COMMAND_SUCCESS,
  META_COMMAND_UNRECOGNIZED_COMMAND
};
typedef enum MetaCommandResult_t MetaCommandResult;

InputBuffer* new_input_buffer();
void print_prompt();
void read_input(InputBuffer* input_buffer);
MetaCommandResult handle_meta_command(InputBuffer* input_buffer, Table* table);
void print_constants();
void print_leaf_node(void* node);

#endif /*REPL_H_*/