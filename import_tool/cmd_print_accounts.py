"""Command for printing all accounts."""

import re
import tabulate

from absl import flags
from moneyflow import accounts_lib
from moneyflow import ui_utils
from third_party import appcommands


class CmdPrintAccounts(appcommands.Cmd):
  """Prints a list of all accounts."""

  def Run(self, argv):
    accounts = accounts_lib.AccountsTable()
    accounts.ReadAll(overwrite=True)
    accounts.Print()
