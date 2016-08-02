"""Objects for managing account information."""


import copy
from collections import deque
import storage_lib
import tabulate


class AccountList(object):
  """Stores a list of accounts."""
  _accounts = deque()

  def __init__(self):
    self._storage = storage_lib.GetStorageTable("accounts")
    self._accounts = self.ReadAll()

  def Add(self, account):
    """Add a new account to the list."""
    if not isinstance(account, Account):
      raise ValueError("Parameter 'account' must be an Account object.")
    account.is_new = True
    self._accounts.append(account)

  def Save(self):
    """Saves account information to storage."""
    for account in self._accounts:
      if account.is_new:
        self._storage.BufferRowForWrite(**account.todict())
    self._storage.WriteBufferedRows()

  def ReadAll(self):
    """Reads account information from storage."""
    return [Account.fromdict(row) for row in self._storage.GetAllRows()]

  def Accounts(self):
    """Generator that returns account information."""
    for account in self._accounts:
      yield account

  def Print(self):
    """Print account information in a table."""
    accounts_table = [a.tolist() for a in self.Accounts()]
    if len(accounts_table) == 0:
      print "No accounts found."
    else:
      accounts_table += self._accounts[0].getlistheadings(
          "Account Name", "Account Number")
      tabulate.tabulate(accounts_table, headers="firstrow", tablefmt="psql")


class Account(object):
  """Account base class."""

  def __init__(self, name, number):
    """Instantiate an account given the account parameters."""
    self.name = name
    self.number = number
    self.is_new = False

  def todict(self):
    return {"account_name": self.name, "account_number": self.number}

  def tolist(self):
    return [self.name, self.number]

  @classmethod
  def fromdict(cls, row):
    return cls(row["account_name"], row["account_number"])

  @classmethod
  def getlistheadings(cls, name_str, number_str):
    """Given strings for the account parameters, returns a list of those
    strings in the same order as tolist().
    """
    return [name_str, number_str]
