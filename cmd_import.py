"""Command execution harness for importing new data."""


from google.apputils import appcommands
import gflags as flags


class CmdImport(appcommands.Cmd):
  """Import command."""

  def Run(self, argv):
    print "Import"
