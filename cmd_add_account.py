"""Command execution harness for importing new data."""


import re

from google.apputils import appcommands
import gflags as flags
import accounts_lib
import tabulate
import ui_utils


class CmdAddAccount(appcommands.Cmd):
  """Adds an account."""

  def Run(self, argv):
    accounts = accounts_lib.AccountList()
    print "Current accounts:"
    accounts.Print()
    acccounts.Add(self._GetAccountFromUser())
    print "New set of accounts:"
    accounts.Print()
    if ui_utils.PromptUser("Are you sure you want to save these accounts?"):
      accounts.Save()
    else:
      print "Accounts not saved."

  def _GetAccountFromUser(self):
    """Returns an Account object based on data gathered from user.

    Raises:
      ValueError: If the account number is invalid.
    """
    name = self._GetAccountNameFromUser()
    number = self._GetAccountFromUser()
    # Validate that the number is a number (assumes no alphabet characters in
    # the account number).
    if re.match("^[0-9]*$", number) is None:
      raise ValueError("Account number is invalid: %r" % number)
    return accounts_lib.Account(input_account_name, input_account_number)

  def _GetAccountNameFromUser(self):
    return raw_input("Enter account name: ")

  def _GetAccountNumberFromUser(self):
    return raw_input("Enter account number: ")
