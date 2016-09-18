"""Tests for transactions_lib."""

import os
import datetime
import mock

import transactions_lib

from google.apputils import basetest
import gflags as flags
import test_utils


FLAGS = flags.FLAGS


class TransactionsTableTest(basetest.TestCase):

  def setUp(self):
    self._fake_storage = test_utils.FakeStorageTable(
        "transactions",
        ["account_number", "transaction_date", "transaction_description",
          "transaction_amount"])
    mock.patch.object(
        transactions_lib.storage_lib, "GetStorageTable",
        return_value=self._fake_storage).start()
    self.addCleanup(mock.patch.stopall)
    self._transactions = transactions_lib.TransactionsTable()

  def testSave(self):
    test_account_num = 134213
    test_date = datetime.date(2004, 9, 24)
    test_description = "This is an epic transaction."
    test_amount = 1222.12

    txn = transactions_lib.Transaction(
        test_account_num, test_date, test_description, test_amount)
    self._transactions.Add(txn)
    self._transactions.Save()

    row = self._fake_storage._ReadRows().next()
    self.assertEqual(test_account_num, int(row["account_number"]))
    self.assertEqual(
        test_date.strftime(transactions_lib.TRANSACTION_DATE_FORMAT),
        row["transaction_date"])
    self.assertEqual(test_description, row["transaction_description"])
    self.assertEqual(test_amount, float(row["transaction_amount"]))

  def testPrint(self):
    test_account_num = 3243
    test_date = datetime.date(2009, 7, 21)
    test_description = "This is an printed transaction."
    test_amount = 4234.34
    self._transactions.Add(
        transactions_lib.Transaction(
          test_account_num, test_date, test_description, test_amount))
    self._transactions.Print()

  def testEq(self):
    txn1 = transactions_lib.Transaction(
        1234, datetime.date(1999, 9, 19), "testeq", 12321.09)
    txn2 = transactions_lib.Transaction(
        1234, datetime.date(1999, 9, 19), "testeq", 12321.09)
    self.assertTrue(txn1 == txn2)

  def testHash(self):
    txn1 = transactions_lib.Transaction(
        41389, datetime.date(2007, 10, 9), "testhash", 328.21)
    txn2 = transactions_lib.Transaction(
        41389, datetime.date(2007, 10, 9), "testhash", 328.21)
    s = set([txn1])
    self.assertTrue(txn2 in s)


class ImportTransactionsTest(basetest.TestCase):

  def testImport(self):
    file_path = os.path.join(
        os.path.dirname(__file__), "testdata/test_import.ofx")
    transactions = transactions_lib.ImportTransactions(file_path)
    self.assertEqual(1, len(transactions))
    t = transactions[0]
    self.assertEqual(1234567, t.account_num)
    self.assertEqual(datetime.date(2016, 9, 15), t.date)
    self.assertEqual("NEW YORK TIMES DIGITAL", t.description)
    self.assertEqual(-15.0, t.amount)



if __name__ == "__main__":
  basetest.main()
