"""Tests for categories_lib."""

import mock

import categories_lib

from google.apputils import basetest
import gflags as flags
import test_utils


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


if __name__ == "__main__":
  basetest.main()
