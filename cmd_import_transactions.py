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
        "file_path", "", "File containing transaction data.",
        flag_values=flag_values)
    super(CmdImportTransactions, self).__init__(name, flag_values, **kwargs)

  def Run(self, argv):
    # Load account info.
    accounts = accounts_lib.AccountsTable()

    # Prompt user to select account
    print "Please select an account from the following list:"
    accounts.Print()
    account_name = ui_utils.GetInputFromUser("Enter an account name: ")
    selected_account = accounts.GetAccount(account_name)
    if selected_account is None:
      print "ERROR: Could not find account %s" % account_name
      return

    # Use account loader to grab transactions
    selected_account.ImportTransactions(csv_file=FLAGS.file_path)

    # Load transaction info.
    # Search for duplicate transactions.
    # Add transactions and prompt user.
    # Save transactions.
