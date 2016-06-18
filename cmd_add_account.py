"""Command execution harness for importing new data."""


from google.apputils import appcommands
import gflags as flags
import accounts_lib
import tabulate


class CmdAddAccount(appcommands.Cmd):
  """Import command."""

  def Run(self, argv):
    accounts = accounts_lib.AccountList()
    print "Current accounts:"
    self.PrintAccounts(accounts)

  def PrintAccounts(self, accounts):
    """Print account information in a table. accounts is an AccountList."""
    accounts_table = [a.tolist() for a in accounts.Accounts()]
    if len(accounts_table) == 0:
      print "No accounts found."
    else:
      accounts_table = accounts.Accounts().getlistheadings() + accounts_table
      tabulate.tabulate(accounts_table, headers="firstrow", tablefmt="psql")
