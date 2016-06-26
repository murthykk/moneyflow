"""Objects for managing account information."""


import copy
import storage_lib


class AccountList(object):
  """Stores a list of accounts."""
  _accounts = []

  def __init__(self):
    self._storage = storage_lib.GetStorageTable("accounts")
    self._accounts = self.ReadAll()

  def Save(self):
    """Saves account information to storage."""
    for account in self._accounts:
      if account.is_new:
        self._storage.BufferRowForWrite(account.todict())
    self._storage.WriteBufferedRows()

  def ReadAll(self):
    """Reads account information from storage."""
    return [Account.fromdict(row) for row in self._storage.GetAllRows()]

  def Accounts(self):
    """Generator that returns account information."""
    for account in self._accounts:
      yield account


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
    return [name, number]
