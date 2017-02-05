"""Main budget script. Controls CSV ingest and adding new vendors/categories."""


from google.apputils import appcommands
import cmd_add_account
import cmd_categorize
import cmd_export_data
import cmd_list_categories
import cmd_print_accounts
import cmd_import_transactions


def main(argv):
  # TODO: Before jumping in to the app, set up the program by asking for a
  # password and reading transactions data.
  # Add a financial account.
  appcommands.AddCmd("add_account", cmd_add_account.CmdAddAccount)
  # Print all accounts.
  appcommands.AddCmd("list_accounts", cmd_print_accounts.CmdPrintAccounts)
  # Import transaction data into an account.
  appcommands.AddCmd(
      "import_transactions", cmd_import_transactions.CmdImportTransactions)
  # Print transaction data.
  #appcommands.AddCmd("print_transactions", CmdPrintTransactions)
  # Categorize transaction data.
  appcommands.AddCmd("categorize", cmd_categorize.CmdCategorize)
  # List categories.
  appcommands.AddCmd("list_categories", cmd_list_categories.CmdListCategories)
  # Export joined data
  appcommands.AddCmd("export_data", cmd_export_data.CmdExportData)


if __name__ == "__main__":
  appcommands.Run()
