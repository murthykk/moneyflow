"""Account information storage in a CSV file."""


import accounts_lib
import csv_storage_lib
import csv_config


class CsvAccountList(AccountList):
  def __init__(self, storage):
    """Instantiates an AccountList from a CSV file specified by filename."""
    with open(filename, "r") as f:
      self._account_list = 

  def _GetStorage(self):
    return csv_storage_lib.CsvStorage(pass)
