#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "repl.h"

int main(int argc, char* argv[]) {
  InputBuffer* input_buffer = new_input_buffer();
  while (true) {
    print_prompt();
    read_input(input_buffer);
    handle_repl_input(input_buffer);
  }
}