"""Command for categorizing transactions."""

from moneyflow import transactions_lib
from moneyflow import ui_utils
from third_party import appcommands


class CmdCategorize(appcommands.Cmd):
  """Categorizes all transactions that have not yet been categorized."""

  def Run(self, argv):
    transactions = transactions_lib.TransactionsTable()
    transactions.ReadAll(overwrite=True)
    ui_utils.CategorizeTransactions(transactions.objects)
