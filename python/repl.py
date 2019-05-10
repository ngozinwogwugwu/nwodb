def handle_meta_commands(meta_command):
  if (meta_command == '.exit'):
    exit('bye!')
  else:
    print('meta command not recognized: ' + meta_command)

def handle_repl_input(user_input):
  if (user_input[0] == '.'):
    handle_meta_commands(user_input)
    return

  # handle normal commands next
  print('your normal command: ' + user_input)

