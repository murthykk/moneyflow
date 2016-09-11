"""Library of objects to access tranactions data."""

import datetime
from collections import deque
import storage_lib
import tabulate


TRANSACTION_DATE_FORMAT = "%Y-%m-%d"


class TransactionsTable(object):
  """Accesses a table of transaction info."""

  _transactions = deque()

  def __init__(self):
    self._storage = storage_lib.GetStorageTable("transactions")
    self._transactions = deque()

  def Add(self, transaction):
    if not isinstance(transaction, Transaction):
      raise ValueError("Argument 'transaction' must be a Transaction object.")
    transaction.is_new = True
    self._transactions.append(transaction)

  def Save(self):
    """Saves transaction information to storage."""
    for transaction in self._transactions:
      if transaction.is_new:
        self._storage.BufferRowForWrite(**transaction.todict())
    self._storage.WriteBufferedRows()

  def ReadAll(self):
    """Reads all transaction info from storage."""
    return deque(
        Transaction.fromdict(row) for row in self._storage.GetAllRows())

  def Print(self, transactions=None):
    """Print transaction information in a table."""
    if transactions is None:
      transactions = self.ReadAll()
      transactions.extend(self._transactions)
    if not isinstance(transactions, deque):
      ValueError("Argument 'transactions' must be a deque of Transaction objs.")
    table = [a.tolist() for a in transactions]
    if len(table) == 0:
      print "No transactions found."
    else:
      table = [
          Transaction.getlistheadings(
              "Account Number", "Date", "Description", "Amount")
          ] + table
      print tabulate.tabulate(
          table, headers="firstrow", tablefmt="psql")


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
