"""Command execution harness for importing new data."""


from google.apputils import appcommands
import gflags as flags


class CmdAddAccount(appcommands.Cmd):
  """Import command."""

  def Run(self, argv):
    print "Add account"
