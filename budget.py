"""Main budget script. Controls CSV ingest and adding new vendors/categories."""


import os
import csv
import shutil
import argparse

from google.apputils import appcommands
import gflags as flags


def main(argv):
  # TODO: Before jumping in to the app, set up the program by asking for a
  # password and reading transactions data.
  # Add a financial account.
  appcommands.AddCmd("add_account", CmdAddAccount)
  # Import transaction data into an account.
  #appcommands.AddCmd("import", CmdImport)
  # Categorize transaction data.
  #appcommands.AddCmd("categorize", CmdCategorize)
  # Print spending report.
  #appcommands.AddCmd("print_report", CmdPrintReport)


if __name__ == "__main__":
  appcommands.Run()
