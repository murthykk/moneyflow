"""Tests for storage_lib."""

import os
import csv
import json
import mock
import uuid

import storage_lib
import test_utils

#from google.apputils import basetest
#import gflags as flags
from absl import flags
from absl.testing import absltest
#from unittest import mock

FLAGS = flags.FLAGS


class StorageTableTest(absltest.TestCase):
  """Tests StorageTable base class."""

  def setUp(self):
    self._fake_rows=[{"column1": "data", "column2": "atad"},
                     {"column1": "word", "column2": "drow"},
                     {"column1": "test", "column2": "tset"}]
    self._fake_columns = ["column1", "column2"]
    self._table = test_utils.FakeStorageTable(
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


class CsvTableTest(absltest.TestCase):
  """Tests CsvTable subclass."""

  _table_name = "test_table"
  _csv_file_name = "test_table.csv"
  _columns = ["some", "test", "columns"]

  def setUp(self):
    self._csv_table = self._GetCsvTable()

  def _GetCsvTable(self, csv_file_path=None):
    if csv_file_path is None:
      FLAGS.csv_base_path = FLAGS.test_tmpdir
      config_file_path = self._WriteStorageConfigFile(self._csv_file_name)
    else:
      FLAGS.csv_base_path = os.path.dirname(csv_file_path)
      config_file_path = self._WriteStorageConfigFile(
          os.path.basename(csv_file_path))

    FLAGS.storage_type = "csv"
    FLAGS.storage_config_file = config_file_path
    return storage_lib.GetStorageTable(self._table_name)

  def _WriteStorageConfigFile(self, rel_path):
    """Writes a storage config file pertinent to this test.

    The config file can be used to instantiate a CsvTable class with the proper
    parameters.
    """
    config_file_path = os.path.join(
        FLAGS.test_tmpdir, "config_{}.json".format(uuid.uuid1()))
    config = {
        self._table_name: {
          "rel_path": rel_path, "columns": self._columns}}
    with open(config_file_path, "w") as f:
      json.dump(config, f)
      self.addCleanup(os.remove, config_file_path)
    return config_file_path

  def testWrite(self):
    data1 = ("1", "2", "3")
    data2 = ("a", "b", "c")
    self._csv_table.BufferRowForWrite(*data1)
    self._csv_table.BufferRowForWrite(*data2)
    self._csv_table.WriteBufferedRows()
    self.addCleanup(os.remove, self._csv_table.file_path)

    with open(self._csv_table.file_path, "r") as f:
      reader = csv.DictReader(f)
      self.assertSameElements(reader.fieldnames, self._columns)
      row1 = next(reader)
      row2 = next(reader)
      for idx,col in enumerate(self._columns):
        self.assertEqual(data1[idx], row1[col])
      for idx,col in enumerate(self._columns):
        self.assertEqual(data2[idx], row2[col])

  def testRead(self):
    table = self._GetCsvTable(
        os.path.join(FLAGS.test_srcdir,
                     "moneyflow/moneyflow/testdata/test_read.csv"))
    exp_row1 = ["132", "12312", "12048"]
    exp_row2 = ["data", "to", "read"]
    with open(table.file_path, "r") as f:
      reader = csv.DictReader(f)
      row1 = next(reader)
      row2 = next(reader)
      for idx,exp in enumerate(exp_row1):
        self.assertEqual(exp, row1[self._columns[idx]])
      for idx,exp in enumerate(exp_row2):
        self.assertEqual(exp, row2[self._columns[idx]])


if __name__ == "__main__":
  absltest.main()
