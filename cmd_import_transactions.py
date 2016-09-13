"""Command for importing transactions."""


import re

from google.apputils import appcommands
import gflags as flags
import accounts_lib
import transactions_lib
import tabulate
import ui_utils


class CmdImportTransactions(appcommands.Cmd):
  """Imports transactions."""

  def __init__(self, name, flag_values, **kwargs):
    flags.DEFINE_string(
        "file_path", "", "File containing transaction data.",
        flag_values=flag_values)
    super(CmdImportTransactions, self).__init__(name, flag_values, **kwargs)

  def Run(self, argv):
    # Load account info.
    accounts = accounts_lib.AccountList()
