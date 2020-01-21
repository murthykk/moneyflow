"""Tests for ui_utils.py."""

import copy
import datetime
import categories_lib
import mock
import test_utils
import transactions_lib
import ui_utils

from absl.testing import absltest


class UserInputTests(absltest.TestCase):
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
  @mock.patch("ui_utils.PromptUser", return_value=False)  # Decline regex cat.
  def testGetCategoryFromUser(self, unused1, unused2):
    transaction_desc = "test trans desc"
    cat = ui_utils._GetCategoryFromUser(transaction_desc)
    self.assertEqual("test cat", cat.category)
    self.assertEqual("disp name", cat.display_name)
    self.assertFalse(cat.is_regex)
    self.assertEqual(transaction_desc, cat.transaction_description)

  @mock.patch("__builtin__.raw_input",
              side_effect=["test trans", "test cat", "disp name"])
  @mock.patch("ui_utils.PromptUser", return_value=True)  # Accept regex cat.
  def testGetRegexCategoryFromUser(self, unused1, unused2):
    """Tests that a valid regex category is returned by _GetCategoryFromUser."""
    transaction_desc = "test trans desc"
    cat = ui_utils._GetCategoryFromUser(transaction_desc)
    self.assertEqual("test cat", cat.category)
    self.assertEqual("disp name", cat.display_name)
    self.assertTrue(cat.is_regex)
    self.assertEqual("test trans", cat.transaction_description)

  @mock.patch("__builtin__.raw_input",
              side_effect=["invalid regex", "another invalid regex"])
  @mock.patch("ui_utils.PromptUser", side_effect=[
      True,  # Yes to regex entry.
      True,  # Yes to try again when first entry fails.
      False  # No to try again after second entry fails.
  ])
  def testGetRegexCategoryFromUser(self, unused1, unused2):
    """Tests that an invalid regex category returns None."""
    transaction_desc = "test trans desc"
    cat = ui_utils._GetCategoryFromUser(transaction_desc)
    self.assertIsNone(cat)



class CategorizationTests(absltest.TestCase):
  """Tests transaction categorization logic."""

  @classmethod
  def setUpClass(cls):
    # The standard categories and transactions below are perfectly matched,
    # in that every transaction has a category and every category has a
    # transaction.
    cls.STANDARD_CATEGORIES = [
        categories_lib.Category("desc 1", "disp 1", "cat 1"),
        categories_lib.Category("desc 2", "disp 2", "cat 2")
    ]
    cls.STANDARD_TRANSACTIONS = [
      transactions_lib.Transaction(
          7, datetime.date(2011, 9, 15), "desc 1", -23.1),
      transactions_lib.Transaction(
          7, datetime.date(2011, 9, 16), "desc 2", -1.33),
      transactions_lib.Transaction(
          7, datetime.date(2011, 9, 17), "desc 1", 30.31)
    ]

  def setUp(self):
    self._fake_storage = test_utils.FakeStorageTable(
        "cateogories",
        ["transaction_description", "display_name", "category"])
    mock.patch.object(
        categories_lib.storage_lib, "GetStorageTable",
        return_value=self._fake_storage).start()
    self.addCleanup(mock.patch.stopall)

  def _AddStandardCategoriesToTable(self, cat_table):
    for cat in self.STANDARD_CATEGORIES:
      cat_table.Add(cat)

  @mock.patch("ui_utils.PromptUser", return_value=False)
  def testAddCategoriesToTransactions_NothingToCategorize(self, unused):
    """Tests that categorization quits immediately if nothing to categorize."""
    cat_table = categories_lib.CategoriesTable()
    self._AddStandardCategoriesToTable(cat_table)
    self.assertTrue(
        ui_utils.AddCategoriesToTransactions(
            cat_table, self.STANDARD_TRANSACTIONS))

  @mock.patch("ui_utils.GetIntegerFromUser", return_value=1)
  @mock.patch("ui_utils.PromptUser", side_effect=[True, True, False])
  def testAddCategoriesToTransactions_AddOneCategory(self, unused1, unused2):
    """Tests that a category can be added."""
    cat_table = categories_lib.CategoriesTable()
    self._AddStandardCategoriesToTable(cat_table)

    # Add an uncategorized transaction to the standard ones.
    new_txn = transactions_lib.Transaction(
        7, datetime.date(2013, 1, 25), "uncategorized desc", -48.49)
    transactions = self.STANDARD_TRANSACTIONS + [new_txn]

    # The following category will be added.
    new_cat = categories_lib.Category(
            "uncategorized desc", "new disp", "new_cat")

    with mock.patch("ui_utils._GetCategoryFromUser", return_value=new_cat):
      self.assertTrue(
          ui_utils.AddCategoriesToTransactions(cat_table, transactions))

    # Make sure one new category was added.
    self.assertEqual(
        len(self.STANDARD_CATEGORIES) + 1, len(cat_table),
        "A new category was not added to the category table.")

    # Find the new category.
    cat_table.InitializeCategoryLookup()
    added_cat = cat_table.GetCategoryForTransaction(new_txn)
    self.assertIsNotNone(
        added_cat,
        "The newly added category is not matched with the uncategorized "
        "transaction.")

    # Make sure the right category information was added.
    self.assertDictEqual(new_cat.todict(), added_cat.todict())

  @mock.patch("ui_utils.GetIntegerFromUser", return_value=1)
  @mock.patch("ui_utils.PromptUser", side_effect=[
      True,  # Yes to "Add a category?"
      True,  # Yes to "Add this category?"
      False  # No to second "Add a category?"
  ])
  def testAddCategoriesToTransactions_AddRegexCategory(self, unused1, unused2):
    """Tests the adding of a regex category."""
    cat_table = categories_lib.CategoriesTable()
    self._AddStandardCategoriesToTable(cat_table)

    # Add a couple of uncategorized transactions to the standard ones.
    transactions = copy.deepcopy(self.STANDARD_TRANSACTIONS)
    new_txn1 = transactions_lib.Transaction(
        7, datetime.date(2015, 4, 21), "uncategorized desc", -3.38)
    transactions += [new_txn1]
    new_txn2 = transactions_lib.Transaction(
        7, datetime.date(2015, 3, 22), "uncategorized desc 1", -9.27)
    transactions += [new_txn2]

    # Add a category that matches the second of the above transactions.
    exact_match_cat = categories_lib.Category(
        "uncategorized desc 1", "UNCAT", "EXISTING CAT", is_regex=False)
    cat_table.Add(exact_match_cat)

    # The following regex category will be added, which should match both of the
    # above new categories. Note that the user will be warned that the category
    # that was just added in the line above already matches a transaction.
    regex_cat = categories_lib.Category(
        "uncategorized", "new disp", "new_cat", is_regex=True)

    with mock.patch("ui_utils._GetCategoryFromUser", return_value=regex_cat):
      self.assertTrue(
          ui_utils.AddCategoriesToTransactions(cat_table, transactions))

    # Make sure the expected number of new categories was added.
    self.assertEqual(
        len(self.STANDARD_CATEGORIES) + 2, len(cat_table),
        "The expected new categories were not added to the category table.")

    # Find the categories for the new transactions.
    cat_table.InitializeCategoryLookup()
    matching_cat1 = cat_table.GetCategoryForTransaction(new_txn1)
    matching_cat2 = cat_table.GetCategoryForTransaction(new_txn2)
    self.assertIsNotNone(matching_cat1)
    self.assertIsNotNone(matching_cat2)

    # Make sure the right category information was added. Note that the first
    # transaction should match the regex, but the second transaction should
    # match exactly the newly added category, which takes precedence over the
    # regex.
    self.assertDictEqual(regex_cat.todict(), matching_cat1.todict())
    self.assertDictEqual(exact_match_cat.todict(), matching_cat2.todict())

  @mock.patch("ui_utils.GetIntegerFromUser", return_value=1)
  @mock.patch("ui_utils.PromptUser", side_effect=[
      True,  # Yes to "Add a category?"
      False  # No to second "Add a category?"
  ])
  def testAddCategoriesToTransactions_UserCancelsCategoryInput(
      self, unused1, unused2):
    """Tests that a category can be added."""
    cat_table = categories_lib.CategoriesTable()
    self._AddStandardCategoriesToTable(cat_table)

    # Add an uncategorized transaction to the standard ones.
    new_txn = transactions_lib.Transaction(
        7, datetime.date(2013, 1, 25), "uncategorized desc", -48.49)
    transactions = self.STANDARD_TRANSACTIONS + [new_txn]

    with mock.patch("ui_utils._GetCategoryFromUser", return_value=None):
      self.assertFalse(
          ui_utils.AddCategoriesToTransactions(cat_table, transactions))

  @mock.patch("ui_utils.PromptUser", return_value=False)
  def testAddCategoriesToTransactions_NotEverythingCategorized(self, unused):
    """Tests case where user quits before everything is categorized."""
    cat_table = categories_lib.CategoriesTable()
    self._AddStandardCategoriesToTable(cat_table)

    # Add an uncategorized transaction to the standard ones.
    new_txn = transactions_lib.Transaction(
        7, datetime.date(2013, 1, 25), "uncategorized desc", -48.49)
    transactions = self.STANDARD_TRANSACTIONS + [new_txn]

    self.assertFalse(
        ui_utils.AddCategoriesToTransactions(cat_table, transactions))


if __name__ == "__main__":
  absltest.main()
