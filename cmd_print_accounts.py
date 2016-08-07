"""Command for printing all accounts."""


import re

from google.apputils import appcommands
import gflags as flags
import accounts_lib
import tabulate
import ui_utils


class CmdPrintAccounts(appcommands.Cmd):
  """Appcommands harness to print a list of all accounts."""

  def Run(self, argv):
    accounts = accounts_lib.AccountList()
    accounts.Print()
