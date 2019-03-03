"""Tests for accounts_lib."""

import accounts_lib

import mock
import test_utils

from absl import flags
from absl.testing import absltest

FLAGS = flags.FLAGS


class AccountsListTest(absltest.TestCase):

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
    test_account_number = 34109
    self._accounts.Add(
        accounts_lib.Account(test_account_name, test_account_number))
    added_account = self._accounts.objects[0]
    self.assertEqual(test_account_name, added_account.name)
    self.assertEqual(test_account_number, added_account.number)

  def testAddInvalidAccount(self):
    with self.assertRaises(ValueError):
      self._accounts.Add("adding a string is invalid.")

  def testSave(self):
    # Add a new account and save it to storage.
    test_account_name = "test_save"
    test_account_number = 14707
    account_obj = accounts_lib.Account(test_account_name, test_account_number)
    self._accounts.Add(account_obj)
    self._accounts.Save()

    # Read the account row from storage and validate it.
    row = next(self._fake_storage._ReadRows())
    self.assertEqual(test_account_name, row["account_name"])
    self.assertEqual(test_account_number, int(row["account_number"]))

  def testPrint(self):
    test_account_name = "test_print"
    test_account_number = 4270382
    self._accounts.Add(
        accounts_lib.Account(test_account_name, test_account_number))
    self._accounts.Print()


if __name__ == "__main__":
  absltest.main()
