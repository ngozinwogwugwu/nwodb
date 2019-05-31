import os
import sys
import unittest
import constants
from io        import StringIO
from table     import Table
from interface import handle_repl_input
from interface import handle_sql_command

DATABASE_NAME = 'test_database'

class TestNwoDB(unittest.TestCase):

  def test_bad_meta_command(self):
    capturedOutput = StringIO()
    table = Table(DATABASE_NAME)

    sys.stdout = capturedOutput
    handle_repl_input('.hi', table)
    sys.stdout = sys.__stdout__

    self.assertEqual(capturedOutput.getvalue(), 'meta command not recognized: .hi\n')
    self.cleanup_db_file(table.pager.file)


  def test_exit_meta_command(self):
    table = Table(DATABASE_NAME)
    with self.assertRaises(SystemExit) as exit_code:
      handle_repl_input('.exit', table)
    self.assertEqual(exit_code.exception.code, 'bye!')


  def test_insert(self):
    table = Table(DATABASE_NAME)
    capturedOutput = StringIO()

    sys.stdout = capturedOutput
    handle_sql_command('insert 1 user user@email.com', table)
    handle_sql_command('insert 2 name name@email.com', table)
    handle_sql_command('select', table)
    sys.stdout = sys.__stdout__

    self.assertEqual(
      capturedOutput.getvalue(),
      "(1, 'user', 'user@email.com')\n(2, 'name', 'name@email.com')\n"
    )
    self.cleanup_db_file(table.pager.file)


  def test_bad_insert_num_arguments(self):
    table = Table(DATABASE_NAME)
    capturedOutput = StringIO()


    sys.stdout = capturedOutput
    handle_sql_command('insert bad', table)
    sys.stdout = sys.__stdout__

    self.assertEqual(
      capturedOutput.getvalue(),
      "PREPARE_SYNTAX_ERROR: the insert command takes three arguments - insert 1 name email@example.com\n"
    )
    self.cleanup_db_file(table.pager.file)

  def test_bad_insert_non_int(self):
    table = Table(DATABASE_NAME)
    capturedOutput = StringIO()

    sys.stdout = capturedOutput
    handle_sql_command('insert one two three', table)
    sys.stdout = sys.__stdout__

    self.assertEqual(
      capturedOutput.getvalue(),
      "Second argument must be an integer\n"
    )
    self.cleanup_db_file(table.pager.file)

  def test_bad_insert_float(self):
    table = Table(DATABASE_NAME)
    capturedOutput = StringIO()

    sys.stdout = capturedOutput
    handle_sql_command('insert 0.3 two three', table)
    sys.stdout = sys.__stdout__

    self.assertEqual(
      capturedOutput.getvalue(),
      "Second argument must be an integer\n"
    )
    self.cleanup_db_file(table.pager.file)

  def test_bad_insert_negative_id(self):
    table = Table(DATABASE_NAME)
    capturedOutput = StringIO()

    sys.stdout = capturedOutput
    handle_sql_command('insert -1 two three', table)
    sys.stdout = sys.__stdout__

    self.assertEqual(
      capturedOutput.getvalue(),
      "row ID must be positive\n"
    )
    self.cleanup_db_file(table.pager.file)


  def test_bad_insert_overlong_name(self):
    table = Table(DATABASE_NAME)
    capturedOutput = StringIO()
    overlong_name = 'onetwothreefourfivesixseveneightnineten'

    sys.stdout = capturedOutput
    handle_sql_command('insert 1 ' + overlong_name + ' three', table)
    sys.stdout = sys.__stdout__

    self.assertEqual(
      capturedOutput.getvalue(),
      "name too long: " + overlong_name + "\n"
    )
    self.cleanup_db_file(table.pager.file)


  def test_bad_insert_overlong_email(self):
    table = Table(DATABASE_NAME)
    capturedOutput = StringIO()
    overlong_email = 'twothreefourfivesixseveneightninetentwothreefourfivesixseveneightninetentwothreefourfivesixseveneightninetentwothreefourfivesixseveneightninetentwothreefourfivesixseveneightninetentwothreefourfivesixseveneightninetentwothreefourfivesixseveneightninetentwothreefourfivesixseveneightnineten'

    sys.stdout = capturedOutput
    handle_sql_command('insert 1 two ' + overlong_email, table)
    sys.stdout = sys.__stdout__

    self.assertEqual(
      capturedOutput.getvalue(),
      "email too long: " + overlong_email + "\n"
    )
    self.cleanup_db_file(table.pager.file)


  def test_bad_insert_table_full(self):
    table = Table(DATABASE_NAME)
    capturedOutput = StringIO()

    # fill up the table
    for i in range(1, constants.TABLE_MAX_ROWS + 1):
      handle_sql_command('insert ' + str(i) + ' two three', table)

    sys.stdout = capturedOutput
    handle_sql_command('insert ' + str(constants.TABLE_MAX_ROWS + 1) + ' two three', table)
    sys.stdout = sys.__stdout__

    self.assertEqual(
      capturedOutput.getvalue(),
      "Error: Table full.\n"
    )
    self.cleanup_db_file(table.pager.file)


  def test_bad_select(self):
    table = Table(DATABASE_NAME)
    capturedOutput = StringIO()

    sys.stdout = capturedOutput
    handle_sql_command('select bad', table)
    sys.stdout = sys.__stdout__

    self.assertEqual(
      capturedOutput.getvalue(),
      "PREPARE_SYNTAX_ERROR: the select command takes no arguments\n"
    )
    self.cleanup_db_file(table.pager.file)


  def test_database_persistence(self):
    # make three inserts, flush the table to disk and end the program
    table = Table(DATABASE_NAME)
    handle_sql_command('insert 12 fourteen fifteen', table)
    handle_sql_command('insert 13 twelve eleven', table)
    handle_sql_command('insert 14 nineteen fifty', table)
    
    with self.assertRaises(SystemExit) as exit_code:
      handle_repl_input('.exit', table)
    self.assertEqual(exit_code.exception.code, 'bye!')

    # select from the table from disk
    capturedOutput = StringIO()
    table_from_disk = Table(DATABASE_NAME)
    sys.stdout = capturedOutput
    handle_sql_command('select', table_from_disk)
    sys.stdout = sys.__stdout__

    # make sure it matches what we put in before
    self.assertEqual(
      capturedOutput.getvalue(),
      "(12, 'fourteen', 'fifteen')\n(13, 'twelve', 'eleven')\n(14, 'nineteen', 'fifty')\n"
    )
    self.cleanup_db_file(table_from_disk.pager.file)


  def cleanup_db_file(self, file):
    file.close()
    os.remove(file.name)

if __name__ == '__main__':
  unittest.main()