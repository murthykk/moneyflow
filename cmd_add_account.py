"""Command execution harness for importing new data."""


from google.apputils import appcommands
import gflags as flags
import accounts_lib


class CmdAddAccount(appcommands.Cmd):
  """Import command."""

  def Run(self, argv):
    accounts = accounts_lib.AccountList()
    print "Add account"
