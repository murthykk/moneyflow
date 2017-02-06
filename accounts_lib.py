"""Objects for managing account information."""


import copy
from collections import deque
import storage_lib
import tabulate


class AccountsTable(storage_lib.ObjectStorage):
  """Accesses a table of account information."""

  def __init__(self):
    super(AccountsTable, self).__init__(
        "accounts", Account, ["Account Name", "Account Number"])

  def GetSetOfAccountNums(self):
    """Returns a set of all available account numbers."""
    account_nums = set()
    for account in self.ReadAll():
      account_nums.add(account.number)
    return account_nums

  def GetAccountForTransaction(self, transaction):
    """Returns the Account object associated with the transaction, or None."""
    accounts_map = {
      acct.number: idx for idx,acct in enumerate(self.objects)
    }
    if transaction.account_num in accounts_map:
      return self.objects[accounts_map[transaction.account_num]]
    else:
      return None


class Account(object):
  """Account base class."""

  def __init__(self, name, number):
    """Instantiate an account given the account parameters."""
    if not isinstance(name, basestring):
      raise ValueError("Argument 'name' must be a string.")
    if not isinstance(number, int):
      raise ValueError("Argument 'number' must be a int.")
    self.name = name
    self.number = number
    self.is_new = False

  def todict(self):
    return {"account_name": self.name, "account_number": str(self.number)}

  def to_native_dict(self):
    return {"account_name": self.name, "account_number": self.number}

  def tolist(self):
    return [self.name, self.number]

  @classmethod
  def fromdict(cls, row):
    return cls(row["account_name"], int(row["account_number"]))

  @classmethod
  def getlistheadings(cls, name_str, number_str):
    """Given strings for the account parameters, returns a list of those
    strings in the same order as tolist().
    """
    return [name_str, number_str]

  def __repr__(self):
    return "name: %r, number: %r, new: %r" % (
        self.name, self.number, self.is_new)
