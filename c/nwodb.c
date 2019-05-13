#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "interface.h"
#include "sql_command_processor.h"
#include "backend.h"

int main(int argc, char* argv[]) {
  InputBuffer* input_buffer = new_input_buffer();
  Table* table = new_table();

  while (true) {
    print_prompt();
    read_input(input_buffer);

    if (input_buffer->buffer[0] == '.') {
      handle_meta_command(input_buffer);
    } else {
      handle_sql_command(input_buffer->buffer, table);
    }
  }
}