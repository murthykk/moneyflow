"""Library of objects to access transaction categories."""

import storage_lib

class CategoriesTable(storage_lib.ObjectStorage):

  _description_map = None

  def __init__(self):
    super(CategoriesTable, self).__init__(
        "categories", Category,
        ["Transaction Description", "Display Name", "Category", "Regex?"])
    self._description_map = None

  def GetSortedCategoryNames(self):
    """Returns a sorted iterable of all categories that exist in the table."""
    return sorted(list(set(
        [cat.category for cat in self.objects]
    )))

  def InitializeCategoryLookup(self):
    """Initializes the object to lookup categories.

    Should be called after reading/adding categories to the table, but before
    calling GetCategoryForTransaction. If the table's contents are changed,
    this method must be called again before further lookups.

    TOOD(murthykk): Do this on instantiation to make this class RAII. If
    there's a method to add categories to an existing table instance,
    add new map entries at the end of the method.
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

    Raises:
      RuntimeException: if this function was called before
      InitializeCategoryLookup
    """
    if self._description_map is None:
      raise RuntimeError(
          "GetCategoryFromTransaction was called before "
          "InitializeCategoryLookUp")
    if transaction.description in self._description_map:
      return self.objects[self._description_map[transaction.description]]
    else:
      return None


class Category(object):
  """Container for category data."""

  # TODO: The transaction descrioption can just be a regex match. Shoiuld compile it as a Python regex first to see if it works.
  # If not, then just use exact match.
  #
  # The tricky bit will be: what happens when multiple categories match a single transaction? This hasn't happened 
  # previously since the description_map unique-ifies the associated transaction description, and the descriptions need to 
  # match exactly. This will essentially end up matching a transaction to the first category. We could continue this but it's
  # more dangerous with regex, as something like (*) can match everything. It would be worth warning if a transaction 
  # matches to more than one category.
  #
  # Actually, the issue with regex is that they can't be applied using the fast hashing lookup that currently 
  # matches categories. So, regex have to be tracked separately.
  transaction_description = ""
  display_name = ""
  category = ""

  is_regex = False
  """True if the transaction_description is a regex instead of an exact match."""

  # Required for all storage objects. This should be in a superclass.
  is_new = False

  def __init__(self, transaction_description, display_name, category, is_regex=False):
    if not isinstance(transaction_description, str):
      raise ValueError("Argument 'transaction_description' must be a string.")
    if not isinstance(display_name, str):
      raise ValueError("Argument 'display_name' must be a string.")
    if not isinstance(category, str):
      raise ValueError("Argument 'category' must be a string.")
    if not isinstance(is_regex, bool):
      # is_regex could be None, and in this case, assume that the description isn't a regex.
      if is_regex is None:
        is_regex = False
      else:
        raise ValueError("Argument 'is_regex' must be a bool or None.")
    self.transaction_description = transaction_description
    self.display_name = display_name
    self.category = category
    self.is_regex = is_regex

  def todict(self):
    return {
        "transaction_description": self.transaction_description,
        "display_name": self.display_name,
        "category": self.category,
        "is_regex": self.is_regex
    }

  def to_native_dict(self):
    return self.todict()

  @classmethod
  def fromdict(cls, row):
    return cls(
        row["transaction_description"], row["display_name"], row["category"], row["is_regex"])

  def tolist(self):
    return [self.transaction_description, self.display_name, self.category, self.is_regex]

  @classmethod
  def getlistheadings(cls, transaction_description, display_name, category, is_regex):
    return [transaction_description, display_name, category, is_regex]
