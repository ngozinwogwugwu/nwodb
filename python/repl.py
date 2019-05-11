from compiler import handle_sql_command

def handle_meta_commands(meta_command):
  if (meta_command == '.exit'):
    exit('bye!')
  else:
    print('meta command not recognized: ' + meta_command)

def handle_repl_input(user_input):
  if (user_input[0] == '.'):
    handle_meta_commands(user_input)
    return

  handle_sql_command(user_input)

