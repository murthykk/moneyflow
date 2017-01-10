"""Tests for categories_lib."""

import datetime
import mock

import categories_lib

from google.apputils import basetest
import gflags as flags
import test_utils
import transactions_lib


FLAGS = flags.FLAGS


class CategoriesTableTest(basetest.TestCase):

  def setUp(self):
    self._fake_storage = test_utils.FakeStorageTable(
        "cateogories",
        ["transaction_description", "display_name", "category"])
    mock.patch.object(
        categories_lib.storage_lib, "GetStorageTable",
        return_value=self._fake_storage).start()
    self.addCleanup(mock.patch.stopall)
    self._categories = categories_lib.CategoriesTable()

  def testSave(self):
    test_description = "This is some transaction"
    test_display_name = "AwesomeTransaction"
    test_category = "Goodness"

    cat = categories_lib.Category(
        test_description, test_display_name, test_category)
    self._categories.Add(cat)
    self._categories.Save()

    row = self._fake_storage._ReadRows().next()
    self.assertEqual(test_description, row["transaction_description"])
    self.assertEqual(test_display_name, row["display_name"])
    self.assertEqual(test_category, row["category"])

  def testPrint(self):
    test_description = "This is a printed transaction"
    test_display_name = "WillfulTransaction"
    test_category = "Sweetness"
    self._categories.Add(
        categories_lib.Category(
            test_description, test_display_name, test_category))
    self._categories.Print()

  def testGetCategoryForTransaction(self):
    test_description = "This transaction should be found"
    test_display_name = "KnownTransaction"
    test_category = "Valid"
    self._categories.Add(
        categories_lib.Category(
            test_description, test_display_name, test_category))
    self._categories.InitializeCategoryLookup()

    cat = self._categories.GetCategoryForTransaction(
        transactions_lib.Transaction(
            0, datetime.date(2008, 3, 4), test_description, 0.0))
    self.assertEqual(test_category, cat.category)

  def testGetCategoryForTransaction_NoCategory(self):
    test_description = "This transaction will not be found"
    test_display_name = "UnknownTransaction"
    test_category = "Invalid"
    self._categories.Add(
        categories_lib.Category(
            test_description, test_display_name, test_category))
    self._categories.InitializeCategoryLookup()

    cat = self._categories.GetCategoryForTransaction(
        transactions_lib.Transaction(
            0, datetime.date(2008, 3, 4), "Unknown description",0.0))
    self.assertIsNone(cat)


if __name__ == "__main__":
  basetest.main()
