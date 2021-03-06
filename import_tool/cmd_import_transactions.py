"""Command for importing transactions."""

import os
import re
import tabulate

from absl import flags
from moneyflow import accounts_lib
from moneyflow import categories_lib
from moneyflow import transactions_lib
from moneyflow import ui_utils
from third_party import appcommands


FLAGS = flags.FLAGS


class CmdImportTransactions(appcommands.Cmd):
  """Imports transactions."""

  def __init__(self, name, flag_values, **kwargs):
    flags.DEFINE_string(
        "ofx_file_path", None, "OFX file containing transaction data.",
        flag_values=flag_values)
    flags.mark_flag_as_required("ofx_file_path", flag_values=flag_values)
    super(CmdImportTransactions, self).__init__(name, flag_values, **kwargs)

  def Run(self, argv):
    account_nums = accounts_lib.AccountsTable().GetSetOfAccountNums()
    existing_transactions = (transactions_lib
                             .TransactionsTable().GetSetOfAllTransactions())
    # Load transaction info.
    new_txns = transactions_lib.ImportTransactions(
        ofx_file=os.path.expanduser(FLAGS.ofx_file_path))

    # Add transactions to the table.
    transactions = transactions_lib.TransactionsTable()
    error = False
    for txn in new_txns:
      if self._CheckIfNewTransactionIsValid(txn, account_nums):
        if self._FilterTransaction(txn, existing_transactions):
          transactions.Add(txn)
      else:
        error = True
    if error:
      print("ERROR: Invalid transactions were found during import. Exiting.")
      return

    # Prompt user and save transactions.
    if len(transactions) > 0:
      print("The following new transactions will be saved:")
      transactions.Print()
      if ui_utils.PromptUser("Save these transactions?"):
        transactions.Save()
        print("Done.")
        print("Starting transaction categorization.")
        ui_utils.CategorizeTransactions(transactions.objects)
      else:
        print("Transactions not saved.")
    else:
      print("No new transactions found.")

  def _CheckIfNewTransactionIsValid(self, transaction, account_nums):
    """Checks if a new transaction is valid. Returns True or False."""
    if transaction.account_num not in account_nums:
      print("ERROR: Unknown account number for transaction {}.".format(
          transaction))
      return False
    return True

  def _FilterTransaction(self, transaction, existing_transactions):
    if transaction in existing_transactions:
      print("Transaction alraedy exists: {}.".format(transaction))
      return False
    return True
