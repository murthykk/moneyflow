"""Lists categories in the system."""


from google.apputils import appcommands
import categories_lib


class CmdListCategories(appcommands.Cmd):
  """Categorizes all transactions that have not yet been categorized."""

  def Run(self, argv):
    categories = categories_lib.CategoriesTable()
    categories.ReadAll(overwrite=True)
    print "The following transaction categories exist:"
    for cat_name in categories.GetSortedCategoryNames():
      print cat_name
