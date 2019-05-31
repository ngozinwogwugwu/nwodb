from interface import get_database_table
from interface import nwodb_prompt

table = get_database_table()
while (True):
  nwodb_prompt(table)