"""Library of objects to access tranactions data."""

import datetime
from collections import deque
import ofxparse
import storage_lib


TRANSACTION_DATE_FORMAT = "%Y-%m-%d"


class Error(Exception):
  """Exception class for this module."""


class TransactionsTable(storage_lib.ObjectStorage):
  """Accesses a table of transaction information."""

  def __init__(self):
    super(TransactionsTable, self).__init__(
        "transactions", Transaction,
        ["Account Number", "Date", "Description", "Amount"])

  def GetSetOfAllTransactions(self):
    """Returns a set containing all transaction objects.

    Raises an error if duplicate transactions exist in the system.
    """
    self.ReadAll()
    txn_set = set(self._objects)
    if len(self._objects) != len(txn_set):
      txn_set = set()
      duplicates = deque()
      for txn in self.objects:
        if txn in txn_set:
          duplicates.append(txn)
        else:
          txn_set.add(txn)
      raise Error("Duplicate transactions exist: %r"
                  % [str(t) for t in duplicates])
    return txn_set


class Transaction(object):
  """Container for transaction data.

  Transaction objects can be hashed and tested for equivalence, in order to
  search for duplicate transactions.
  """

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

  def __eq__(self, other):
    """Transactions are duplicate if all fields are the same."""
    return (
        self.account_num == other.account_num
        and self.date == other.date
        and self.description == other.description
        and self.amount == other.amount)

  def __hash__(self):
    """Hash all fields."""
    return hash(
        "{}_{}_{}_{:.2f}".format(
            self.account_num,
            self.date.strftime(TRANSACTION_DATE_FORMAT),
            self.description,
            self.amount))

  def __repr__(self):
    return "account: %r, date: %r, description: %r, amount: %r" % (
        self.account_num, self.date.strftime(TRANSACTION_DATE_FORMAT),
        self.description, self.amount)

  @classmethod
  def getlistheadings(
      cls, account_num_str, date_str, description_str, amount_str):
    return [account_num_str, date_str, description_str, amount_str]

  @classmethod
  def fromdict(cls, row):
    return cls(
        int(row["account_number"]),
        datetime.datetime.strptime(
          row["transaction_date"], TRANSACTION_DATE_FORMAT).date(),
        row["transaction_description"], float(row["transaction_amount"]))

  def __repr__(self):
    """Return string representation of this object."""
    return str(self.todict())

  def __str__(self):
    return self.__repr__()


def ImportTransactions(ofx_file):
  """Import transatction data from an OFX file.

  Returns:
    A deque of transactions.
  """
  # Parse the OFX file.
  with open(ofx_file, "r") as f:
    ofx = ofxparse.OfxParser.parse(f)
  account_number = ofx.account.number

  # Convert the parsed file to Transaction objects
  transactions = deque()
  for ofx_txn in ofx.account.statement.transactions:
    transactions.append(
        Transaction(int(account_number),
                    ofx_txn.date.date(),
                    ofx_txn.payee.upper(),
                    float(ofx_txn.amount)))

  return transactions
