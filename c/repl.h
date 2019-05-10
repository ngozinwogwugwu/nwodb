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

struct InputBuffer_t {
  char* buffer;
  size_t buffer_length;
  ssize_t input_length;
};
typedef struct InputBuffer_t InputBuffer;

InputBuffer* new_input_buffer();
void print_prompt();
void read_input(InputBuffer* input_buffer);
void close_input_buffer(InputBuffer* input_buffer);

#endif /*REPL_H_*/