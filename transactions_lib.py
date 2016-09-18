"""Library of objects to access tranactions data."""

import datetime
from collections import deque
import storage_lib


TRANSACTION_DATE_FORMAT = "%Y-%m-%d"


class TransactionsTable(storage_lib.ObjectStorage):
  """Accesses a table of transaction information."""

  def __init__(self):
    super(TransactionsTable, self).__init__(
        "transactions", Transaction,
        ["Account Number", "Date", "Description", "Amount"])


class Transaction(object):
  """Container for transaction data."""

  account_num = 0
  date = None
  description = ""
  amount = 0.0
  is_new = False

  def __init__(self, account_num, date, description, amount):
    if not isinstance(date, datetime.date):
      raise ValueError("Argument 'date' must be a datetime.date object.")
    if not isinstance(account_num, int):
      raise ValueError("Argument 'account_num' must be an int.")
    if not isinstance(description, basestring):
      raise ValueError("Argument 'description' must be a string.")
    if not isinstance(amount, float):
      raise ValueError("Argument 'amount' must be a float.")
    self.account_num = account_num
    self.date = date
    self.description = description
    self.amount = amount
    self.is_new = False

  def todict(self):
    return {
        "account_number": str(self.account_num),
        "transaction_date": self.date.strftime(TRANSACTION_DATE_FORMAT),
        "transaction_description": self.description,
        "transaction_amount": str(self.amount)
    }

  def tolist(self):
    return [self.account_num, self.date, self.description, self.amount]

  @classmethod
  def getlistheadings(
      cls, account_num_str, date_str, description_str, amount_str):
    return [account_num_str, date_str, description_str, amount_str]

  @classmethod
  def fromdict(cls, row):
    return cls(
        int(row["account_num"]),
        datetime.strptime(
          row["transaction_date"], TRANSACTION_DATE_FORMAT).date(),
        row["transaction_description"], float(row["transaction_amount"]))
