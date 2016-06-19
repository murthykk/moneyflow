"""Tests for storage_lib."""

import mock

import storage_lib
from google.apputils import basetest


class StorageTest(basetest.TestCase):
  """Tests Storage base class."""

  def setUp(self):
    self._storage = storage_lib.Storage("test", "column1", "column2")

  def testGetAllRows(self):
    pass

  def testBufferRowForWrite(self):
    pass

  def testBufferInvalidRowForWrite(self):
    pass

  def testWriteBufferedRows(self):
    pass

  def testIterator(self):
    pass


if __name__ == "__main__":
  basetest.main()
