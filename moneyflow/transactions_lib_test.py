"""Tests for transactions_lib."""

import transactions_lib

import os
import datetime
import mock
import test_utils

from absl import flags
from absl.testing import absltest


FLAGS = flags.FLAGS


class TransactionsTableTest(absltest.TestCase):

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

    row = next(self._fake_storage._ReadRows())
    self.assertEqual(test_account_num, int(row["account_number"]))
    self.assertEqual(
        test_date.strftime(transactions_lib.TRANSACTION_DATE_FORMAT),
        row["transaction_date"])
    self.assertEqual(test_description, row["transaction_description"])
    self.assertEqual(test_amount, float(row["transaction_amount"]))

  def testGetSetOfAllTransactions(self):
    test_account_num = 312098
    test_date = datetime.date(2007, 3, 13)
    test_description = "This is an hashed transaction."
    test_amount = -41.23
    txn = transactions_lib.Transaction(
        test_account_num, test_date, test_description, test_amount)
    self._transactions.Add(txn)
    self._transactions.Save()

    txn_set = self._transactions.GetSetOfAllTransactions()
    self.assertEqual(1, len(txn_set))

    txn2 = transactions_lib.Transaction(
        test_account_num, test_date, test_description, test_amount)
    self.assertTrue(txn2 in txn_set)


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


class ImportTransactionsTest(absltest.TestCase):

  def testImport(self):
    file_path = os.path.join(
        FLAGS.test_srcdir, "moneyflow/moneyflow/testdata/test_import.ofx")
    transactions = transactions_lib.ImportTransactions(file_path)
    self.assertEqual(1, len(transactions))
    t = transactions[0]
    self.assertEqual(1234567, t.account_num)
    self.assertEqual(datetime.date(2016, 9, 15), t.date)
    self.assertEqual("NEW YORK TIMES DIGITAL", t.description)
    self.assertEqual(-15.0, t.amount)



if __name__ == "__main__":
  absltest.main()
