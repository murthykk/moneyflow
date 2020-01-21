"""Tests for categories_lib."""

import categories_lib

import datetime
import mock
import test_utils
import transactions_lib

from absl.testing import absltest


class CategoriesTableTest(absltest.TestCase):

  def setUp(self):
    self._fake_storage = test_utils.FakeStorageTable(
        "cateogories",
        ["transaction_description", "display_name", "category", "is_regex"])
    mock.patch.object(
        categories_lib.storage_lib, "GetStorageTable",
        return_value=self._fake_storage).start()
    self.addCleanup(mock.patch.stopall)
    self._categories = categories_lib.CategoriesTable()

  def testSave(self):
    test_description = "This is some transaction"
    test_display_name = "AwesomeTransaction"
    test_category = "Goodness"
    test_is_regex = True

    cat = categories_lib.Category(
        test_description, test_display_name, test_category, test_is_regex)
    self._categories.Add(cat)
    self._categories.Save()

    row = next(self._fake_storage._ReadRows())
    self.assertEqual(test_description, row["transaction_description"])
    self.assertEqual(test_display_name, row["display_name"])
    self.assertEqual(test_category, row["category"])
    self.assertEqual(test_is_regex, bool(row["is_regex"]))

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

  def testGetCategoryForTransaction_Regex(self):
    test_description = "Transaction regex and more"
    test_regex = "Transaction regex"
    test_display_name = "AnotherTransaction"
    test_category = "SomeCategory"
    self._categories.Add(
        categories_lib.Category(
            test_regex, test_display_name, test_category, is_regex=True))

    self._categories.InitializeCategoryLookup()
    cat = self._categories.GetCategoryForTransaction(
        transactions_lib.Transaction(
            0, datetime.date(2008, 3, 4), test_description, 0.0))
    self.assertEqual(test_category, cat.category)

  def testGetCategoryForTransaction_RegexIgnoresCase(self):
    test_description = "tRANSACTION REGEX aND mOre"
    test_regex = "transaction regex"
    test_display_name = "AnotherTransaction"
    test_category = "SomeCategory"
    self._categories.Add(
        categories_lib.Category(
            test_regex, test_display_name, test_category, is_regex=True))

    self._categories.InitializeCategoryLookup()
    cat = self._categories.GetCategoryForTransaction(
        transactions_lib.Transaction(
            0, datetime.date(2008, 3, 4), test_description, 0.0))
    self.assertEqual(test_category, cat.category)

  def testGetCategoryForTransaction_RegexDoesntMatch(self):
    test_description = "Transaction regex"
    test_display_name = "AnotherTransaction"
    test_category = "SomeCategory"
    self._categories.Add(
        categories_lib.Category(
            test_description, test_display_name, test_category, is_regex=True))

    self._categories.InitializeCategoryLookup()
    cat = self._categories.GetCategoryForTransaction(
        transactions_lib.Transaction(
            0, datetime.date(2008, 3, 4), "Transaction", 0.0))
    self.assertIsNone(cat)

  def testGetCategoryForTransaction_ExactMatchOverRegex(self):
    """Tests that exact match category takes precedence over a regex match."""
    test_description = "Transaction regex and more"
    test_regex = "Transaction regex"
    test_display_name = "AnotherTransaction"
    regex_category = "RegexCategory"
    exact_category = "ExactCategory"

    # Add a regex category and an exact match category.
    self._categories.Add(
        categories_lib.Category(
            test_regex, test_display_name, regex_category, is_regex=True))
    self._categories.Add(
        categories_lib.Category(
            test_description, test_display_name, exact_category,
            is_regex=False))

    self._categories.InitializeCategoryLookup()
    cat = self._categories.GetCategoryForTransaction(
        transactions_lib.Transaction(
            0, datetime.date(2008, 3, 4), test_description, 0.0))
    self.assertEqual(exact_category, cat.category)


if __name__ == "__main__":
  absltest.main()
