"""Lists categories in the system."""

from moneyflow import categories_lib
from third_party import appcommands


class CmdListCategories(appcommands.Cmd):
  """Categorizes all transactions that have not yet been categorized."""

  def Run(self, argv):
    categories = categories_lib.CategoriesTable()
    categories.ReadAll(overwrite=True)
    print("The following transaction categories exist:")
    for cat_name in categories.GetSortedCategoryNames():
      print(cat_name)
