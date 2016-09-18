"""Command for importing transactions."""


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
        "ofx_file_path", "", "OFX file containing transaction data.",
        flag_values=flag_values)
    super(CmdImportTransactions, self).__init__(name, flag_values, **kwargs)

  def Run(self, argv):
    # Load transaction info.
    new_txns = transactions_lib.ImportTransactions(ofx_file=FLAGS.ofx_file_path)

    # Make sure the account number exists for all transactions.
    account_nums = accounts_lib.AccountsTable().GetSetOfAccountNums()
    for txn in new_txns:
      if txn.account_num not in account_nums:
        print "ERROR: Unknown account number {} for transaction {}.".format(
            txn.account_number, str(txn))

    # TODO: Search for duplicate transactions.

    # Add transactions.
    transactions = transactions_lib.TransactionsTable()
    for txn in new_txns:
      transactions.Add(txn)

    # Prompt user and save transactions.
    print "The following new transactions will be saved:"
    transactions.Print()
    if ui_utils.PromptUser("Save these transactions?"):
      transactions.Save()
    else:
      print "Transactions not saved."
