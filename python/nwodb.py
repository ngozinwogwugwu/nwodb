import sys
from repl import handle_repl_input
from compiler import handle_sql_command

tree = [];

while (True):
  user_input = handle_repl_input()
  handle_sql_command(user_input, tree)