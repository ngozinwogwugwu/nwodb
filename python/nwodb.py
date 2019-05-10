import sys
from repl import handle_repl_input

while (True):
  user_input = input('nwodb >>> ')
  handle_repl_input(user_input)
