#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "interface.h"
#include "sql_command_processor.h"
#include "backend.h"

int main(int argc, char* argv[]) {
  InputBuffer* input_buffer = new_input_buffer();

  if (argc < 2) {
      printf("Must supply a database filename.\n");
      exit(EXIT_FAILURE);
  }

  char* filename = argv[1];
  Table* table = db_open(filename);

  while (true) {
    print_prompt();
    read_input(input_buffer);

    if (input_buffer->buffer[0] == '.') {
      handle_meta_command(input_buffer, table);
    } else {
      handle_sql_command(input_buffer->buffer, table);
    }
  }
}