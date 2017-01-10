"""Library of objects to access transaction categories."""

import storage_lib

class CategoriesTable(storage_lib.ObjectStorage):

  _description_map = None

  def __init__(self):
    super(CategoriesTable, self).__init__(
        "categories", Category,
        ["Transaction Description", "Display Name", "Category"])
    self._description_map = None

  def InitializeCategoryLookup(self):
    """Initializes the object to lookup categories.

    Should be called after reading/adding categories to the table, but before
    calling GetCategoryForTransaction. If the table's contents are changed,
    this method must be called again before further lookups.
    """
    self._description_map = {
      cat.transaction_description: idx for idx,cat in enumerate(self.objects)
    }

  def GetCategoryForTransaction(self, transaction):
    """Returns the category for the given transaction object.

    This method searches categories that are stored in this object.

    Args:
      transaction: A Transaction object whose category is needed.

    Returns:
      A single Category object associated with the transaction, or None if no
      category could be found.
    """
    if transaction.description in self._description_map:
      return self.objects[self._description_map[transaction.description]]
    else:
      return None


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
