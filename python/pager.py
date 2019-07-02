import os
import math
import constants

class Pager:

  def __init__(self, filename):
    mode = 'r+b' if os.path.exists(filename) else 'w+b'
    self.file = open(filename, mode)
    self.file_length = os.stat(filename).st_size
    self.num_pages = math.ceil(self.file_length/constants.PAGE_SIZE)
    self.pages = [None] * constants.TABLE_MAX_PAGES

  def close(self):
    self.file.close()

  def load_or_create_page(self, page_num):
    # get number of full and incomplete pages in the file

    # if there is incomplete page data in the file, read it into page
    if (page_num <= self.num_pages):
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

  def overwrite_page(self, node, page_num):
    self.pages[page_num] = node.serialize()


  def insert_new_page(self, node):
    node.serialize()
    page_num = self.get_unused_page_num()
    self.pages[page_num] = node.page
    self.num_pages += 1

    return page_num


  def flush_page(self, page_num):
    page = self.get_page(page_num)
    if (page == None):
      exit('Tried to flush null page')

    self.file.seek(page_num * constants.PAGE_SIZE)
    self.file.write(page)

  def get_unused_page_num(self):
    return self.num_pages