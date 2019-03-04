"""Command for categorizing transactions."""


from google.apputils import appcommands
import transactions_lib
import ui_utils


class CmdCategorize(appcommands.Cmd):
  """Categorizes all transactions that have not yet been categorized."""

  def Run(self, argv):
    transactions = transactions_lib.TransactionsTable()
    transactions.ReadAll(overwrite=True)
    ui_utils.CategorizeTransactions(transactions.objects)
