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
    self._accounts = accounts_lib.AccountsTable()

  def testAdd(self):
    test_account_name = "test_add"
    test_account_number = "34109"
    self._accounts.Add(
        accounts_lib.Account(test_account_name, test_account_number))
    added_account = self._accounts.Accounts().next()
    self.assertEqual(test_account_name, added_account.name)
    self.assertEqual(test_account_number, added_account.number)

  def testAddInvalidAccount(self):
    with self.assertRaises(ValueError):
      self._accounts.Add("adding a string is invalid.")

  def testSave(self):
    # Add a new account and save it to storage.
    test_account_name = "test_save"
    test_account_number = "014707"
    account_obj = accounts_lib.Account(test_account_name, test_account_number)
    self._accounts.Add(account_obj)
    self._accounts.Save()

    # Read the account row from storage and validate it.
    row = self._fake_storage._ReadRows().next()
    self.assertEqual(test_account_name, row["account_name"])
    self.assertEqual(test_account_number, row["account_number"])

  def testPrint(self):
    test_account_name = "test_print"
    test_account_number = "4270382"
    self._accounts.Add(
        accounts_lib.Account(test_account_name, test_account_number))
    self._accounts.Print()


if __name__ == "__main__":
  basetest.main()
