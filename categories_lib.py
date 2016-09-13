"""Library of objects to access transaction categories."""

import datetime
from collections import deque
import storage_lib
import tabulate


class CategoriesTable(storage_lib.ObjectStorage):

  def __init__(self):
    super(CategoriesTable, self).__init__(
        "categories", Category,
        ["Transaction Description", "Display Name", "Category"])


class Category(object):
  """Container for category data."""

  transaction_description = ""
  display_name = ""
  category = ""
  is_new = False

  def __init__(self, transaction_description, display_name, category):
    if not isinstance(transaction_description, basestring):
      raise ValueError("Argument 'transaction_description' must be a string.")
    if not isinstance(display_name, basestring):
      raise ValueError("Argument 'display_name' must be a string.")
    if not isinstance(category, basestring):
      raise ValueError("Argument 'category' must be a string.")
    self.transaction_description = transaction_description
    self.display_name = display_name
    self.category = category

  def todict(self):
    return {
        "transaction_description": self.transaction_description,
        "display_name": self.display_name,
        "category": self.category
    }

  @classmethod
  def fromdict(cls, row):
    return cls(
        row["transaction_description"], row["display_name"], row["category"])

  def tolist(self):
    return [self.transaction_description, self.display_name, self.category]

  @classmethod
  def getlistheadings(cls, transaction_description, display_name, category):
    return [transaction_description, display_name, category]
