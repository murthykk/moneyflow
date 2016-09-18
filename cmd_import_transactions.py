"""Command for importing transactions."""

import os
import re

from google.apputils import appcommands
import gflags as flags
import accounts_lib
import transactions_lib
import tabulate
import ui_utils


FLAGS = flags.FLAGS


class CmdImportTransactions(appcommands.Cmd):
  """Imports transactions."""

  def __init__(self, name, flag_values, **kwargs):
    flags.DEFINE_string(
        "ofx_file_path", None, "OFX file containing transaction data.",
        flag_values=flag_values)
    flags.MarkFlagAsRequired("ofx_file_path", flag_values=flag_values)
    super(CmdImportTransactions, self).__init__(name, flag_values, **kwargs)
    self._account_nums = accounts_lib.AccountsTable().GetSetOfAccountNums()
    self._all_transactions = (transactions_lib
        .TransactionsTable().GetSetOfAllTransactions())

  def Run(self, argv):
    # Load transaction info.
    new_txns = transactions_lib.ImportTransactions(
        ofx_file=os.path.expanduser(FLAGS.ofx_file_path))

    # Add transactions to the table.
    transactions = transactions_lib.TransactionsTable()
    error = False
    for txn in new_txns:
      if self._CheckIfNewTransactionIsValid(txn):
        transactions.Add(txn)
      else:
        error = True
    if error:
      print "ERROR: Invalid transactions were found during import. Exiting."
      return

    # Prompt user and save transactions.
    print "The following new transactions will be saved:"
    transactions.Print()
    if ui_utils.PromptUser("Save these transactions?"):
      transactions.Save()
      print "Done."
    else:
      print "Transactions not saved."

  def _CheckIfNewTransactionIsValid(self, transaction):
    """Checks if a new transaction is valid. Returns True or False."""
    if transaction.account_num not in self._account_nums:
      print "ERROR: Unknown account number for transaction {}.".format(
          transaction)
      return False
    if transaction in self._all_transactions:
      print "ERROR: Transaction alraedy exists: {}.".format(transaction)
      return False
    return True
