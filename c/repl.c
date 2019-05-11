#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "repl.h"
#include "compiler.h"

InputBuffer* new_input_buffer() {
  InputBuffer* input_buffer = malloc(sizeof(InputBuffer));
  input_buffer->buffer = NULL;
  input_buffer->buffer_length = 0;
  input_buffer->input_length = 0;

  return input_buffer;
}

void print_prompt() { printf("nwodb > "); }

void read_input(InputBuffer* input_buffer) {
  ssize_t bytes_read =
      getline(&(input_buffer->buffer), &(input_buffer->buffer_length), stdin);

  if (bytes_read <= 0) {
    printf("Error reading input\n");
    exit(EXIT_FAILURE);
  }

  // Ignore trailing newline
  input_buffer->input_length = bytes_read - 1;
  input_buffer->buffer[bytes_read - 1] = 0;
}

void close_input_buffer(InputBuffer* input_buffer) {
    free(input_buffer->buffer);
    free(input_buffer);
}

MetaCommandResult handle_meta_command(InputBuffer* input_buffer) {
  if (strcmp(input_buffer->buffer, ".exit") == 0) {
    close_input_buffer(input_buffer);
    exit(EXIT_SUCCESS);
  } else {
    printf("Unrecognized command '%s'\n", input_buffer->buffer);
    return META_COMMAND_UNRECOGNIZED_COMMAND;
  }
}

void handle_repl_input(InputBuffer* input_buffer) {
  // handle meta commands
  if (input_buffer->buffer[0] == '.') {
    handle_meta_command(input_buffer);
  } else {
    handle_sql_command(input_buffer->buffer);
  }
}
