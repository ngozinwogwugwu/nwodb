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

  def execute(self):
    if self.statement_type in self.command_executions:
      self.command_executions[self.statement_type]()
      return

    print(self.statement_type + " is not a valid command")

  def handle_insert_command(self):
    print("this is an insert command. ")

  def handle_select_command(self):
    print("this is a select command. ")
