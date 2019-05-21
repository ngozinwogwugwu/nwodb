import sys
import unittest
import constants
from io            import StringIO
from repl          import handle_repl_input
from compiler      import handle_sql_command

class TestNwoDB(unittest.TestCase):

  def test_bad_meta_command(self):
    capturedOutput = StringIO()

    sys.stdout = capturedOutput
    handle_repl_input('.hi')
    sys.stdout = sys.__stdout__

    self.assertEqual(capturedOutput.getvalue(), 'meta command not recognized: .hi\n')


  def test_exit_meta_command(self):
    with self.assertRaises(SystemExit) as exit_code:
      handle_repl_input('.exit')
    self.assertEqual(exit_code.exception.code, 'bye!')


  def test_insert(self):
    tree = [];
    capturedOutput = StringIO()

    sys.stdout = capturedOutput
    handle_sql_command('insert 1 user user@email.com', tree)
    handle_sql_command('insert 2 name name@email.com', tree)
    handle_sql_command('select', tree)
    sys.stdout = sys.__stdout__

    self.assertEqual(
      capturedOutput.getvalue(),
      "[1, 'user', 'user@email.com']\n[2, 'name', 'name@email.com']\n"
    )


  def test_bad_insert_num_arguments(self):
    capturedOutput = StringIO()

    sys.stdout = capturedOutput
    handle_sql_command('insert bad', [])
    sys.stdout = sys.__stdout__

    self.assertEqual(
      capturedOutput.getvalue(),
      "PREPARE_SYNTAX_ERROR: the insert command takes three arguments - input 1 name email@example.com\n"
    )

  def test_bad_insert_non_int(self):
    capturedOutput = StringIO()

    sys.stdout = capturedOutput
    handle_sql_command('insert one two three', [])
    sys.stdout = sys.__stdout__

    self.assertEqual(
      capturedOutput.getvalue(),
      "Second argument must be an integer\n"
    )

  def test_bad_insert_float(self):
    capturedOutput = StringIO()

    sys.stdout = capturedOutput
    handle_sql_command('insert 0.3 two three', [])
    sys.stdout = sys.__stdout__

    self.assertEqual(
      capturedOutput.getvalue(),
      "Second argument must be an integer\n"
    )

  def test_bad_insert_negative_int(self):
    capturedOutput = StringIO()

    sys.stdout = capturedOutput
    handle_sql_command('insert -1 two three', [])
    sys.stdout = sys.__stdout__

    self.assertEqual(
      capturedOutput.getvalue(),
      "row ID must be positive\n"
    )


  def test_bad_insert_table_full(self):
    capturedOutput = StringIO()
    tree = []

    # fill up the table
    for i in range(1, constants.TABLE_MAX_ROWS + 1):
      handle_sql_command('insert ' + str(i) + ' two three', tree)


    sys.stdout = capturedOutput
    handle_sql_command('insert ' + str(constants.TABLE_MAX_ROWS + 1) + ' two three', tree)
    sys.stdout = sys.__stdout__

    self.assertEqual(
      capturedOutput.getvalue(),
      "Error: Table full.\n"
    )


  def test_bad_select(self):
    capturedOutput = StringIO()

    sys.stdout = capturedOutput
    handle_sql_command('select bad', [])
    sys.stdout = sys.__stdout__

    self.assertEqual(
      capturedOutput.getvalue(),
      "PREPARE_SYNTAX_ERROR: the select command takes no arguments\n"
    )


if __name__ == '__main__':
  unittest.main()