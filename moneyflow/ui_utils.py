"""Utilities that help interface with users."""

import re
from collections import deque
import tabulate

import categories_lib
import transactions_lib


def PromptUser(msg):
  while True:
    ans = raw_input("{} [y/n]: ".format(msg)).upper()
    if ans == "Y":
      return True
    elif ans == "N":
      return False
    else:
      print("Please enter a valid response (y or n).")
      continue


def GetIntegerFromUser(msg, lower, upper):
  """Prompt user to enter an integer within bounds.

  Args:
    msg: Message to display when prompting the user.
    lower: Lower bound on the integer (inclusive).
    upper: Upper bound on the integer (inclusive).

  Returns:
    The integer entered by the user.

  Raises:
    ValueError: If user entered invalid input.
  """
  idx = raw_input("{} [{} - {}]: ".format(msg, lower, upper))
  idx = int(idx)
  if idx < lower or idx > upper:
    raise ValueError(
        "Out of range: {} is not in [{} - {}]".format(idx, lower, upper))
  return idx


def CategorizeTransactions(transactions):
  """Check that all transactions have categories.

  If there are uncategorized transactions, the user is offered the
  opportunity to add category information.

  Args:
    transactions: An iterable of Transaction objects to categorize.
  """
  if len(transactions) == 0:
    "No transactions to categorize."
    return

  cat_table = categories_lib.CategoriesTable()
  cat_table.ReadAll(overwrite=True)

  AddCategoriesToTransactions(cat_table, transactions)
  print("Saving newly added categories.")
  cat_table.Save()


def AddCategoriesToTransactions(cat_table, transactions):
  """Prompts user to add category objects for uncategorized transactions.

  This function runs a loop that interacts with the user. In each iteration,
  the user enters information for a new category against an uncategorized
  transaction. The new category is added to the category table. It is then
  used to attempt to categorize all remaining transactions. The loop exits
  when no uncategorized transactions exist, or if the user quits.

  Args:
    cat_table: The CategoryTable containing all categories to start with.
    transacitons: Iterable of Transaction objects to categorize.

  Returns:
    True if all transactions have categories. False if some transactions
    remain uncategorized.
  """
  # Cached table of all existing transactions in case the user enters a new
  # regex category before. In this case, it should be checked against all
  # existing transactions.
  transactions_table = None
  while True:
    # For every transaction, check if a category exists.
    cat_table.InitializeCategoryLookup()
    categories = deque()
    uncat_txns = deque()
    for txn in transactions:
      cat = cat_table.GetCategoryForTransaction(txn)
      if cat is None:
        uncat_txns.append(txn)
        categories.append(cat)

    print("Uncategorized transactions and their categories:")
    PrintTransactionCategories(list(zip(uncat_txns, categories)))

    if None not in set(categories):
      print("All transactions have categories - quitting categorization.")
      return True

    # Offer user chance to add categories.
    if PromptUser("Add a category?"):
      try:
        idx = GetIntegerFromUser(
            "Select a transaction index", 1, len(uncat_txns))
        idx -= 1
        cat = _GetCategoryFromUser(uncat_txns[idx].description)
        if cat is None:
          continue
        # If the category is a regex, print additional info that will help
        # the user make a decision about whether to keep it.
        if cat.is_regex:
          if transactions_table is None:
            transactions_table = transactions_lib.TransactionsTable()
            transactions_table.ReadAll(overwrite=True)
          _PrintRegexCategoryInfo(cat, transactions_table)
      except ValueError as e:
        print("Invalid input. Problem: %s" % str(e))
        continue
      except IndexError:
        print("Input out of range, please try again.")
        continue
      print("New Category:")
      PrettyPrintCategory(cat)
      if PromptUser("Add this category?"):
        cat_table.Add(cat)
    else:
      print("Quitting transaction categorization.")
      return False


def _PrintRegexCategoryInfo(category, transactions_table):
  """Prints info that helps the user verify a regex category.

  Args:
    category: A regex category, where category.is_regex is True.
    transactions_table: A fully populated transactions_lib.TransactionsTable
      that will be used to verify the regex category with the user.

  Raises:
    ValueError: if category.is_regex is False.
  """
  if not category.is_regex:
    raise ValueError("category.is_regex must be True.")
  matching_transactions = transactions_lib.TransactionsTable()
  regex = categories_lib.CompileRegex(category.transaction_description)
  for transaction in transactions_table.objects:
    if categories_lib.MatchRegexObj(regex, transaction.description):
      matching_transactions.Add(transaction)
    # TODO: Also find other existing categories that match this same transaction.

  print("Transactions that match the regex category (%s):" %
        category.transaction_description)
  matching_transactions.Print()


def PrintTransactionCategories(transactions_and_categories):
  """Prints categories associated with each transaction.

  Args:
    transactions_and_categories: Iterable of Transaction object + Category
        object tuples.
  """
  if len(transactions_and_categories) == 0:
    return

  def get_cols(t):
    """Returns a list of strings from rows in a joined transaction/category."""
    txn = t[0].todict()
    if t[1] is not None:
      cat = t[1].todict()
      return [
        txn["transaction_date"],
        txn["transaction_description"],
        txn["transaction_amount"],
        cat["category"]
      ]
    else:
      return [
        txn["transaction_date"],
        txn["transaction_description"],
        txn["transaction_amount"],
        "None"
      ]

  table = [["Index", "Date", "Description", "Amount", "Category"]] + [
    [idx + 1] + get_cols(t) for idx,t in enumerate(transactions_and_categories)
    ]

  print(tabulate.tabulate(table, headers="firstrow", tablefmt="psql"))


def _GetRegexCategory(transaction_description):
  """Queries the user for a regex associated with the transaction description.

  The regex is guaranteed to at least match the description.

  Args:
    transaction_description: The transaction description string.

  Returns:
    A regex string that matches the transaction description, or None if the
    user canceled.
  """
  while True:
    regex = raw_input("Enter regex (Python syntax): ")
    if categories_lib.MatchRegexStr(regex):
      return regex
    print("Regex %s does not match transaction description.")
    if not PromptUser("Try again?"):
      return None


def _GetCategoryFromUser(transaction_description):
  """Asks user for category information, and returns a Category object.

  Returns None if the user canceled.
  """
  is_regex = False
  if PromptUser("Enter regex for transaction description?"):
    regex = _GetRegexCategory(transaction_description)
    if regex is None:
      return None
    transaction_description = regex
    is_regex = True
  else:
    print(
      "What is the category associated with transactions that have the following "
      "description?")
    print(transaction_description)
  category = raw_input("Enter the category's name: ")
  display_name = raw_input("Enter the display name for the transaction: ")
  return categories_lib.Category(
      transaction_description, display_name, category, is_regex)


def PrettyPrintCategory(category):
  """Pretty prints information in a Category object."""
  tmp = categories_lib.CategoriesTable()
  tmp.Add(category)
  tmp.Print()
