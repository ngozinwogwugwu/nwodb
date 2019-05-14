from sql_statement import SQL_Statement

def handle_sql_command(user_input, tree):
  sql_statement = SQL_Statement(user_input)
  sql_statement.prepare()
  sql_statement.execute(tree)

