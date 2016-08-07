"""Main budget script. Controls CSV ingest and adding new vendors/categories."""


import os
import csv
import shutil
import argparse

from google.apputils import appcommands
import cmd_add_account
import cmd_print_accounts
import gflags as flags


def main(argv):
  # TODO: Before jumping in to the app, set up the program by asking for a
  # password and reading transactions data.
  # Add a financial account.
  appcommands.AddCmd("add_account", cmd_add_account.CmdAddAccount)
  # Print all accounts.
  appcommands.AddCmd("list_accounts", cmd_print_accounts.CmdPrintAccounts)
  # Import transaction data into an account.
  #appcommands.AddCmd("import", CmdImportTransactions)
  # Print transaction daata.
  #appcommands.AddCmd("import", CmdPrintTransactions)
  # Categorize transaction data.
  #appcommands.AddCmd("categorize", CmdCategorize)


if __name__ == "__main__":
  appcommands.Run()
