"""Command for exporting joined transaction data to a CSV file."""

import csv
import os

from collections import deque
from google.apputils import appcommands
import gflags as flags
import accounts_lib
import transactions_lib
import categories_lib


FLAGS = flags.FLAGS


class CmdExportData(appcommands.Cmd):
  """Export joined data."""

  def __init__(self, name, flag_values, **kwargs):
    flags.DEFINE_string(
        "output_path", None, "Path for output csv file.",
        flag_values=flag_values)
    flags.MarkFlagAsRequired("output_path", flag_values=flag_values)
    super(CmdExportData, self).__init__(name, flag_values, **kwargs)

  def Run(self, unused_argv):
    accounts = accounts_lib.AccountsTable()
    accounts.ReadAll(overwrite=True)
    categories = categories_lib.CategoriesTable()
    categories.ReadAll(overwrite=True)
    categories.InitializeCategoryLookup()

    with open(os.path.expanduser(FLAGS.output_path), "wb") as f:
      writer = csv.writer(f)
      writer.writerow(self._GetColumnHeaders())
      for txn in transactions_lib.TransactionsTable().ReadAll():
        writer.writerow(self._JoinColumns(txn, accounts, categories))

  def _JoinColumns(self, transaction, accounts_table, categories_table):
    """Joins the transaction data with accounts and category data.

    Args:
      transaction: Transaction object to join
      accounts_table: AccountsTable object with accounts to join against.
      categories_table: CategoriesTable object with categories to join against.

    Returns:
      List representing columns of joined data, in string format.
    """
    t = transaction.todict()
    acct = accounts_table.GetAccountForTransaction(transaction)
    cat = categories_table.GetCategoryForTransaction(transaction)

    if acct is not None:
      a = acct.todict()
      acct_cols = [
        a["account_name"]
      ]
    else:
      acct_cols = [None]

    if cat is not None:
      c = cat.todict()
      cat_cols = [
        c["category"],
        c["display_name"]
      ]
    else:
      cat_cols = [None, None]

    return acct_cols + [
      t["account_number"],
      t["transaction_date"],
      t["transaction_description"],
      t["transaction_amount"],
    ] + cat_cols

  def _GetColumnHeaders(self):
    """Returns list of headers for columns returned by _JoinColumns."""
    return [
      "account_name",
      "account_number",
      "transaction_date",
      "transaction_description",
      "transaction_amount",
      "category",
      "display_name"
    ]
