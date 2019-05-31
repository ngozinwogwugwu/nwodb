import sys
from sql_statement import SQL_Statement
from table import Table

def get_database_table():
  if (len(sys.argv) < 2):
    exit("database name required.")

  return Table(sys.argv[1])


def handle_sql_command(sql_command, table):
  sql_statement = SQL_Statement(sql_command)
  sql_statement.execute(table)


def handle_meta_commands(meta_command, table):
  if (meta_command == '.exit'):
    table.flush()
    exit('bye!')
  else:
    print('meta command not recognized: ' + meta_command)

def handle_repl_input(user_input, table):
  if (user_input[0] == '.'):
    handle_meta_commands(user_input, table)

  return user_input

def nwodb_prompt(table):
  sql_command = handle_repl_input(input('nwodb >>> '), table)
  handle_sql_command(sql_command, table)
