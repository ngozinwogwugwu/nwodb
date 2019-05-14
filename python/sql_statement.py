import pickle

class SQL_Statement:
  def __init__(self, sql_string):
    self.sql_string_array = sql_string.split()
    self.statement_type = None
    self.command_executions = {
      'insert': self.handle_insert_command,
      'select': self.handle_select_command
    }

  def prepare(self):
    self.statement_type = self.sql_string_array[0]

  def execute(self, tree):
    if self.statement_type not in self.command_executions:
      print(self.statement_type + " is not a valid command")
      return
    
    self.command_executions[self.statement_type](tree)


  def handle_insert_command(self, tree):
    ## serialize the tokens into a byte array
    insert_row = self.format_insert_command(self.sql_string_array)
    if insert_row:
      tree.append(pickle.dumps(insert_row))
    

  def format_insert_command(self, sql_string_array):
    insert_row = []
    if len(sql_string_array) != 4:
      print("PREPARE_SYNTAX_ERROR: the insert command takes three arguments - input 1 name email@example.com")
      return False

    try:
      insert_row.append(int(sql_string_array[1]))
    except ValueError:
      print("Second argument must be an integer")
      return False

    insert_row.append(sql_string_array[2]) # append username
    insert_row.append(sql_string_array[3]) # append email
    return insert_row

  def handle_select_command(self, tree):
    for row in tree:
      print(pickle.loads(row))
