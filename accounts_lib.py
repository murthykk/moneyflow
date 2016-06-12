"""Objects for managing account information."""


import copy


class AccountList(object):
  """Stores a list of accounts."""
  _account_list = []

  def Save(self):
    """Saves account information to storage."""
    # TODO

  def ReadAll(self):
    """Reads account information from storage."""
    # TODO

  def GetCopyOfList(self):
    return copy.deepcopy(self._account_list)

  def _GetStorage(self):
    self.



class Account(object):
  """Account base class."""

  def __init__(self, name, number):
    """Instantiate an account given the account parameters."""
    self._name = name
    self._number = number

  def GetName(self):
    """Returns the account name."""
    return self._name

  def GetNumber(self):
    """Returns the account number."""
    return self._number

  @classmethod
  def fromdict(cls, row):
    return cls(row["account_name"], row["account_number"])


