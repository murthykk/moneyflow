"""Tests for storage_lib."""

import os
import json
import mock

import storage_lib
import gflags as flags
from google.apputils import basetest


FLAGS = flags.FLAGS


class FakeStorageTable(storage_lib.StorageTable):
  """Fake storage class used for testing."""

  _fake_rows = None

  def __init__(self, table_name, columns, **kwargs):
    super(FakeStorageTable, self).__init__(table_name, columns)
    if "fake_rows" in kwargs.keys():
      self._fake_rows = kwargs["fake_rows"]

  def _ReadRows(self):
    for row in self._fake_rows:
      yield row

  def _WriteBuffer(self):
    self._fake_rows += self._buffer
    self._buffer = []


class StorageTableTest(basetest.TestCase):
  """Tests StorageTable base class."""

  def setUp(self):
    self._fake_rows=[{"column1": "data", "column2": "atad"},
                     {"column1": "word", "column2": "drow"},
                     {"column1": "test", "column2": "tset"}]
    self._fake_columns = ["column1", "column2"]
    self._table = FakeStorageTable(
        "test", self._fake_columns, fake_rows=self._fake_rows)

  def testGetAllRows(self):
    rows = self._table.GetAllRows()
    self.assertSameElements(self._fake_rows, rows)

  def testBufferedWriteWithArgs(self):
    new_row = {self._fake_columns[0]: "late", self._fake_columns[1]: "etal"}
    self._table.BufferRowForWrite(
        new_row[self._fake_columns[0]], new_row[self._fake_columns[1]])
    self._table.WriteBufferedRows()
    self.assertSameElements(
        self._fake_rows + [new_row], self._table.GetAllRows())

  def testBufferedWriteWithKwargs(self):
    new_row = {self._fake_columns[0]: "late", self._fake_columns[1]: "etal"}
    self._table.BufferRowForWrite(**new_row)
    self._table.WriteBufferedRows()
    self.assertSameElements(
        self._fake_rows + [new_row], self._table.GetAllRows())

  def testBufferInvalidRowForWriteWithArgs(self):
    bad_data = ("fads") * (len(self._fake_columns) + 1)
    with self.assertRaises(ValueError):
      self._table.BufferRowForWrite(*bad_data)

  def testBufferInvalidRowForWriteWithKwargs(self):
    bad_data = {"not_a_column": "any_data"}
    with self.assertRaises(ValueError):
      self._table.BufferRowForWrite(**bad_data)

  def testWriteRow(self):
    # Buffer rows, since the buffer should be preserved on the Write call.
    new_row = {self._fake_columns[0]: "late", self._fake_columns[1]: "etal"}
    self._table.BufferRowForWrite(**new_row)
    self._table.BufferRowForWrite(**new_row)
    self.assertEqual(2, self._table.NumBufferedRows())

    new_row = {self._fake_columns[0]: "hotel", self._fake_columns[1]: "letoh"}
    self._table.WriteRow(**new_row)
    self.assertSameElements(
        self._fake_rows + [new_row], self._table.GetAllRows())

    # Check that the buffer still is OK.
    self.assertEqual(2, self._table.NumBufferedRows())

  def testWriteRowWithWriteError(self):
    """Verifies that the buffer isn't affected when _WriteRows doesn't work."""
    # Buffer rows, since the buffer should be preserved on the Write call.
    new_row = {self._fake_columns[0]: "late", self._fake_columns[1]: "etal"}
    self._table.BufferRowForWrite(**new_row)
    self._table.BufferRowForWrite(**new_row)
    self.assertEqual(2, self._table.NumBufferedRows())

    new_row = {self._fake_columns[0]: "hotel", self._fake_columns[1]: "letoh"}
    with mock.patch.object(
        self._table, "_WriteBuffer", side_effect=storage_lib.Error):
      with self.assertRaises(storage_lib.Error):
        self._table.WriteRow(**new_row)

    # Check that the buffer was preserved.
    self.assertEqual(2, self._table.NumBufferedRows())

  def testIterator(self):
    """Test the iterator methods in StorageTable."""
    # Use the iterator to convert storage table to a list.
    iter_rows = [r for r in self._table]
    self.assertSameElements(self._fake_rows, iter_rows)


class CsvTableTest(basetest.TestCase):
  """Tests CsvTable subclass."""

  _table_name = "test_table"
  _csv_file_name = "csv_test_table.csv"
  _columns = ["some", "test", "columns"]

  def _WriteStorageConfigFile(self):
    """Writes a storage config file pertinent to this test.

    The config file can be used to instantiate a CsvTable class with the proper
    parameters.
    """
    config_file_path = os.path.join(
        FLAGS.test_tmpdir, "test_storage_config.json")
    config = {
        self._table_name: {
          "rel_path": self._csv_file_name, "columns": self._columns}}
    with open(config_file_path, "w") as f:
      json.dump(config, f)
    return config_file_path

  def setUp(self):
    FLAGS.storage_type = "csv"
    FLAGS.csv_base_path = FLAGS.test_tmpdir
    config_file_path = self._WriteStorageConfigFile()
    FLAGS.storage_config_file = config_file_path
    self.addCleanup(os.remove, config_file_path)
    self._csv_table = storage_lib.GetStorageTable(self._table_name)

  def testSomething(self):
    pass


if __name__ == "__main__":
  basetest.main()
