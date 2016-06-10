"""Main budget script. Controls CSV ingest and adding new vendors/categories."""

import os
import csv
import shutil
import argparse

from google.apputils import appcommands
import gflags as flags

class CmdImport(appcommands.Cmd):
  """Import command."""

  def Run(self, argv):
    print "Import"

def main(argv):
  appcommands.AddCmd("import", CmdImport)

if __name__ == "__main__":
  appcommands.Run()
