"""Utilities that help interface with users."""


import categories_lib
from collections import deque
import tabulate


def PromptUser(msg):
  while True:
    ans = raw_input("{} [Y/n]: ".format(msg)).upper()
    if ans == "Y":
      return True
    elif ans == "N":
      return False
    else:
      print "Please enter a valid response (y or n)."
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
  print "Saving newly added categories."
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

    print "Uncategorized transactions and their categories:"
    PrintTransactionCategories(zip(uncat_txns, categories))

    if None not in set(categories):
      print "All transactions have categories - quitting categorization."
      return True

    # Offer user chance to add categories.
    if PromptUser("Add a category?"):
      try:
        idx = GetIntegerFromUser(
            "Select a transaction index", 1, len(uncat_txns))
        idx -= 1
        cat = GetCategoryFromUser(uncat_txns[idx].description)
      except ValueError as e:
        print "Invalid input. Problem: %s" % str(e)
        continue
      except IndexError:
        print "Input out of range, please try again."
        continue
      print "New Category:"
      PrettyPrintCategory(cat)
      if PromptUser("Add this category?"):
        cat_table.Add(cat)
    else:
      print "Quitting transaction categorization."
      return False


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

  print tabulate.tabulate(table, headers="firstrow", tablefmt="psql")


def GetCategoryFromUser(transaction_description):
  """Asks user for category information, and returns a Category object."""
  print(
    "What is the category associated with transactions that have the following "
    "description?")
  print(transaction_description)
  category = raw_input("Enter the category's name: ")
  display_name = raw_input("Enter the display name for the transaction: ")
  return categories_lib.Category(
      transaction_description, display_name, category)


def PrettyPrintCategory(category):
  """Pretty prints information in a Category object."""
  tmp = categories_lib.CategoriesTable()
  tmp.Add(category)
  tmp.Print()
