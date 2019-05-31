import os
import math
import constants

class Pager:

  def __init__(self, filename):
    mode = 'r+b' if os.path.exists(filename) else 'w+b'
    self.file = open(filename, mode)
    self.file_length = os.stat(filename).st_size
    self.pages = [None] * constants.TABLE_MAX_PAGES

  def close(self):
    self.file.close()

  def load_or_create_page(self, page_num):
    # get number of full and incomplete pages in the file
    num_pages = math.ceil(self.file_length/constants.PAGE_SIZE)

    # if there is incomplete page data in the file, read it into page
    if (page_num <= num_pages):
      self.file.seek(page_num * constants.PAGE_SIZE)
      return bytearray(self.file.read(constants.PAGE_SIZE))

    return bytearray()

  def get_page(self, page_num):
    # make sure that the page isn't out of bounds
    if (page_num > constants.TABLE_MAX_PAGES):
      exit('Tried to fetch page number out of bounds. ' + page_num + ' > ' + constants.TABLE_MAX_PAGES)

    # if the page isn't already loaded up, get it from disk (or make a blank one)
    if (self.pages[page_num] == None):
      self.pages[page_num] = self.load_or_create_page(page_num)

    return self.pages[page_num]

  def flush_page(self, page_num):
    if (self.pages[page_num] == None):
      exit('Tried to flush null page')

    self.file.seek(page_num * constants.PAGE_SIZE)
    self.file.write(self.pages[page_num])
