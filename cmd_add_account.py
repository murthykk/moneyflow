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
    # TODO: Gather account info from user
    input_account_name = "test"
    input_account_number = "3242343"
    # TODO: Add account to AccountList
    acccounts.Add(
        accounts_lib.Account(input_account_name, input_account_number))
    print "New set of accounts:"
    self.PrintAccounts(accounts)
    # TODO: Prompt user for confirmation
    accounts.Save()

  def PrintAccounts(self, accounts):
    """Print account information in a table. accounts is an AccountList."""
    accounts_table = [a.tolist() for a in accounts.Accounts()]
    if len(accounts_table) == 0:
      print "No accounts found."
    else:
      accounts_table = accounts.Accounts().getlistheadings() + accounts_table
      tabulate.tabulate(accounts_table, headers="firstrow", tablefmt="psql")
