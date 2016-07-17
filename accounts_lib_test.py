"""Tests for accounts_lib."""

import mock

import accounts_lib
from google.apputils import basetest
import gflags as flags
import test_utils


FLAGS = flags.FLAGS


class AccountsListTest(basetest.TestCase):

  def setUp(self):
    self._fake_storage = test_utils.FakeStorageTable(
        "accounts", ["account_name", "account_number"])
    mock.patch.object(
        accounts_lib.storage_lib, "GetStorageTable",
        return_value=self._fake_storage).start()
    self.addCleanup(mock.patch.stopall)
    self._accounts = accounts_lib.AccountList()

  def testAdd(self):
    pass

  def testSave(self):
    pass

  def testPrint(self):
    pass


if __name__ == "__main__":
  basetest.main()
