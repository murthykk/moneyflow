"""Utilities that help interface with users."""


from collections import deque
import tabulate


def PromptUser(msg):
  ans = raw_input("{} [Y/n]: ".format(msg))
  if ans == "Y":
    return True
  else:
    return False


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

  # Read all categories.
  cat_table = CategoriesTable()
  cat_table.ReadAll(overwrite=True)
  cat_table.InitializeCategoryLookup()

  # For every transaction, check if a category exists.
  categories = deque()
  for txn in transactions:
    categories.append(cat_table.GetCategoryForTransaction(txn))

  # Print results
  print "Transactions and their initial categories:"
  PrintTransactionCategories(zip(transactions, categories))

  # Offer user chance to add categories.
  if PromptUser("Add categories to transactions without categories?"):
    AddCategoriesToTransactions(cat_table, transactions)


def PrintTransactionCategories(transactions_and_categories):
  """Prints categories associated with each transaction.

  Args:
    transactions_and_categories: Iterable of Transaction object + Category
        object tuples.
  """
  if len(transactions_and_categories) == 0:
    return

  def get_cols(t):
    txn = t[0].todict()
    if cat is not None:
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

  table = ["Date", "Description", "Amount", "Category"] + [
    get_cols(t) for t in transactions_and_categories
  ]

  print tabulate.tabulate(table, headers="firstrow", tablefmt="psql")


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
    Updated CategoryTable.
  """
