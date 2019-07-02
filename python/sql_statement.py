import math
import constants

from table     import Table
from row       import Row
from vm        import VM

class SQL_Statement:
  def __init__(self, sql_string):
    self.sql_string_array = sql_string.split()
    self.statement_type = self.sql_string_array[0]
    self.command_executions = {
      'insert': self.handle_insert_command,
      'select': self.handle_select_command
    }
    self.vm = VM()

  def execute(self, table):
    if self.statement_type not in self.command_executions:
      print(self.statement_type + " is not a valid command")
      return
    
    self.command_executions[self.statement_type](table)


  def handle_insert_command(self, table):
    # format the row to insert
    row = self.get_row_from_insert_command()

    if not row:
      return
    self.vm.insert_row(row, table)


  def handle_select_command(self, table):
    if (self.validate_select_command()):
      self.vm.select_all_rows(table)

  def get_row_from_insert_command(self):
    if len(self.sql_string_array) != 4:
      print("PREPARE_SYNTAX_ERROR: the insert command takes three arguments - insert 1 name email@example.com")
      return False

    ## validate input ID
    try:
      user_id = int(self.sql_string_array[1])

      if (user_id <= 0):
        print("row ID must be positive")
        return False

    except ValueError:
      print("Second argument must be an integer")
      return False

    ## validate input name
    name = self.sql_string_array[2]
    if (len(name) > constants.NAME_FIELD_SIZE):
      print("name too long: " + name)
      return False

    ## validate input email
    email = self.sql_string_array[3]
    if (len(email) > constants.EMAIL_FIELD_SIZE):
      print("email too long: " + email)
      return False

    row = Row(user_id, name, email)
    row.serialize()
    return row


  def validate_select_command(self):
    if len(self.sql_string_array) != 1:
      print("PREPARE_SYNTAX_ERROR: the select command takes no arguments")
      return False

    return True