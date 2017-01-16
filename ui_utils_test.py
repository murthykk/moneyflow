"""Tests for ui_utils.py."""

import datetime
import mock

from google.apputils import basetest
import categories_lib
import test_utils
import transactions_lib
import ui_utils


class UserInputTests(basetest.TestCase):
  """Tests methods that get input from user in ui_utils module."""

  @mock.patch("__builtin__.raw_input", return_value="y")
  def testPromptUserTrue(self, unused):
    self.assertTrue(ui_utils.PromptUser("test message"))

  @mock.patch("__builtin__.raw_input", return_value="N")
  def testPromptUserFalse(self, unused):
    self.assertFalse(ui_utils.PromptUser("test 2 message"))

  @mock.patch("__builtin__.raw_input", return_value="3")
  def testGetIntegerFromUser(self, unused):
    self.assertEqual(3, ui_utils.GetIntegerFromUser("get int", 1, 5))

  @mock.patch("__builtin__.raw_input", return_value="10")
  def testGetIntegerFromUserOutOfBounds(self, unused):
    with self.assertRaises(ValueError):
      ui_utils.GetIntegerFromUser("get int", 1, 5)

  @mock.patch("__builtin__.raw_input", return_value="a word")
  def testGetIntegerFromUserInvalidInput(self, unused):
    with self.assertRaises(ValueError):
      ui_utils.GetIntegerFromUser("get int", 1, 5)

  @mock.patch("__builtin__.raw_input", side_effect=["test cat", "disp name"])
  def testGetCategoryFromUser(self, unused):
    transaction_desc = "test trans desc"
    cat = ui_utils.GetCategoryFromUser(transaction_desc)
    self.assertEqual("test cat", cat.category)
    self.assertEqual("disp name", cat.display_name)
    self.assertEqual(transaction_desc, cat.transaction_description)


class CategorizationTests(basetest.TestCase):
  """Tests transaction categorization logic."""

  def setUp(self):
    self._fake_storage = test_utils.FakeStorageTable(
        "cateogories",
        ["transaction_description", "display_name", "category"])
    mock.patch.object(
        categories_lib.storage_lib, "GetStorageTable",
        return_value=self._fake_storage).start()
    self.addCleanup(mock.patch.stopall)

  @mock.patch("ui_utils.PromptUser", return_value=False)
  def testAddCategoriesToTransactions_NothingToCategorize(self, prompt):
    cat_table = categories_lib.CategoriesTable()

    # Add categories to the category table.
    cat_table.Add(
        categories_lib.Category("desc 1", "disp 1", "cat 1"))
    cat_table.Add(
        categories_lib.Category("desc 2", "disp 2", "cat 2"))

    # The following transactions should all have categories.
    transactions = [
        transactions_lib.Transaction(
            7, datetime.date(2011, 9, 15), "desc 1", -23.1),
        transactions_lib.Transaction(
            7, datetime.date(2011, 9, 16), "desc 2", -1.33),
        transactions_lib.Transaction(
            7, datetime.date(2011, 9, 17), "desc 1", 30.31)
    ]

    ui_utils.AddCategoriesToTransactions(cat_table, transactions)

    # The user should not have been prompted to add transactions
    prompt.assert_not_called()


if __name__ == "__main__":
  basetest.main()
