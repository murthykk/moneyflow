"""Library of objects to access transaction categories."""

import re
import storage_lib


class CompiledRegex(object):
  """Thin wrapper around regex compilation for transaction description matching.

  Enforces that all matching ignores case.
  """

  def __init__(self, regex_string):
    self._r = re.compile(regex_string, re.IGNORECASE)

  def match(self, match_str):
    """Wrapper around re.match(). Returns a match object."""
    return self._r.match(match_str)


def MatchRegexObj(regex, transaction_description):
  """Returns true if the regex matches the transaction description.

  Args:
    regex: Compiled regex object.

  Returns:
    True if the regex matches the transaction description, using re.match().

  Raises:
    ValueError if regex is not a re.RegexObject.
  """
  if not isinstance(regex, CompiledRegex):
    raise ValueError("'regex' must be a CompiledRegex.")
  m = regex.match(transaction_description)
  return bool(m)


def MatchRegexStr(regex_str, transaction_description):
  """Returns True if the regex string matches the transaction descrption.

  Args:
    regex_str: Regex string.

  Returns:
    True if the regex matches the transaction description, using re.match().
  """
  return MatchRegexObj(CompiledRegex(regex_str), transaction_description)


class CategoriesTable(storage_lib.ObjectStorage):

  _description_map = None
  """Dict that maps transation descriptions to table indices."""

  _regexes = None
  """List of tuples containing regex objects and the associated table indices."""

  def __init__(self):
    super(CategoriesTable, self).__init__(
        "categories", Category,
        ["Transaction Description", "Display Name", "Category", "Regex?"])
    self._description_map = None
    self._regexes = None

  def GetSortedCategoryNames(self):
    """Returns a sorted iterable of all categories that exist in the table."""
    return sorted(set(cat.category for cat in self.objects))

  def InitializeCategoryLookup(self):
    """Initializes the object to lookup categories.

    Should be called after reading/adding categories to the table, but before
    calling GetCategoryForTransaction. If the table's contents are changed,
    this method must be called again before further lookups.

    TOOD(murthykk): Do this on instantiation to make this class RAII. If
    there's a method to add categories to an existing table instance,
    add new map entries at the end of the method.

    Raises:
      RuntimeError: if an invalid regex category was found.
    """
    self._description_map = {}
    self._regexes = []
    for idx, cat in enumerate(self.objects):
      if not cat.is_regex:
        self._description_map[cat.transaction_description] = idx
      else:
        try:
          self._regexes.append(
              (CompiledRegex(cat.transaction_description), idx))
        except re.error as e:
          raise RuntimeError("Found invalid regular expression: %s" % e.pattern)

  def _MatchRegexes(self, transaction_description):
    """Returns a Category that regex-matches the transaction_description.

    If no regexes match, returns None.

    Args:
      transaction_description: the transaction description string.
    """
    for r, idx in self._regexes:
      if MatchRegexObj(r, transaction_description):
        return self.objects[idx]
    return None

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
      return self._MatchRegexes(transaction.description)


class Category(object):
  """Container for category data."""

  transaction_description = ""
  display_name = ""
  category = ""

  is_regex = False
  """True if the transaction_description is a regex instead of an exact match.
  
  The regex matching ignores case.
  """

  # Required for all storage objects. This should be in a superclass.
  is_new = False

  def __init__(self, transaction_description, display_name, category, is_regex=None):
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
        "is_regex": str(self.is_regex)
    }

  def to_native_dict(self):
    return self.todict()

  @classmethod
  def fromdict(cls, row):
    return cls(
        row["transaction_description"], row["display_name"], row["category"],
        bool(row["is_regex"]))

  def tolist(self):
    return [self.transaction_description, self.display_name, self.category,
            self.is_regex]

  @classmethod
  def getlistheadings(
      cls, transaction_description, display_name, category, is_regex):
    return [transaction_description, display_name, category, is_regex]
