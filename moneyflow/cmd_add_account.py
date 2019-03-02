"""Command for adding a new account."""


import re

from google.apputils import appcommands
import gflags as flags
import accounts_lib
import tabulate
import ui_utils


class CmdAddAccount(appcommands.Cmd):
  """Adds an account."""

  def Run(self, argv):
    accounts = accounts_lib.AccountsTable()
    accounts.ReadAll(overwrite=True)
    print("Current accounts:")
    accounts.Print()
    accounts.Add(self._GetAccountFromUser())
    print("New set of accounts:")
    accounts.Print()
    if ui_utils.PromptUser("Are you sure you want to save these accounts?"):
      accounts.Save()
    else:
      print("Accounts not saved.")

  def _GetAccountFromUser(self):
    """Returns an Account object based on data gathered from user.

    Raises:
      ValueError: If the account number is invalid.
    """
    name = self._GetAccountNameFromUser()
    number = self._GetAccountNumberFromUser()
    # Validate that the number is a number (assumes no alphabet characters in
    # the account number).
    if re.match("^[0-9]*$", number) is None:
      raise ValueError("Account number is invalid: %r" % number)
    return accounts_lib.Account(name, int(number))

  def _GetAccountNameFromUser(self):
    return input("Enter account name: ")

  def _GetAccountNumberFromUser(self):
    return input("Enter account number: ")
