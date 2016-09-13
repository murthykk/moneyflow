"""Set of classes tha handle data storage.

Note: none of the classes below are thread-safe.
"""

import os
from collections import deque
import csv
import json
import gflags as flags
import shutil
import tabulate


STORAGE_TYPES = ["csv"]


flags.DEFINE_enum(
    "storage_type", "csv", STORAGE_TYPES, "Type of backend storage to use.")
flags.DEFINE_string(
    "storage_config_file", "storage_config.json",
    "Base directory where all CSVs will be stored.")
flags.DEFINE_string(
    "csv_base_path", "csvdata",
    "Path to base directory where all CSVs will be stored.")


FLAGS = flags.FLAGS


class Error(Exception):
  """Exception type for this module."""


def GetStorageTable(table_name):
  """Returns a storage interface object, given a storage config object."""
  config = StorageConfig.fromconfigfile(FLAGS.storage_config_file, table_name)
  if FLAGS.storage_type == "csv":
    return CsvTable(config)


class ObjectStorage(object):
  """Accesses deserialized objects from a storage backend.

  The object class must be passed in to obj_cls, and it must implement:
    todict
    fromdict
    tolist
    getlistheadings
  """

  _objects = deque()

  def __init__(self, table_name, obj_cls, table_headings):
    self._storage = GetStorageTable(table_name)
    self._objects = deque()
    self._obj_cls = obj_cls
    self._table_headings = table_headings

  def Add(self, obj):
    if not isinstance(obj, self._obj_cls):
      raise ValueError("Must add a %s object." % self._obj_cls.__name__)
    obj.is_new = True
    self._objects.append(obj)

  def Save(self):
    """Saves object information to storage."""
    for obj in self._objects:
      if obj.is_new:
        self._storage.BufferRowForWrite(**obj.todict())
    self._storage.WriteBufferedRows()

  def ReadAll(self):
    """Reads all object info from storage."""
    return deque(
        self._obj_cls.fromdict(row) for row in self._storage.GetAllRows())

  def Print(self):
    """Print object information in a table."""
    objects = self.ReadAll()
    objects.extend(self._objects)
    table = [a.tolist() for a in objects]
    if len(table) == 0:
      print "No object found."
    else:
      table = [
          self._obj_cls.getlistheadings(*self._table_headings)] + table
      print tabulate.tabulate(
          table, headers="firstrow", tablefmt="psql")


class StorageConfig(object):
  def __init__(self, config_dict):
    """Initialize config object with parameters."""
    self.rel_path = config_dict["rel_path"]
    self.columns = config_dict["columns"]

  @classmethod
  def fromconfigfile(cls, config_file, storage_name):
    with open(config_file, "r") as f:
      config_json = json.load(f)
    return cls(config_json[storage_name])


class StorageTable(object):
  """Class to interface with a storage table.

  This base class hides the implementation of the storage internals. It allows
  users to store tables in different formats depending on the subclass.

  Subclasses must override the following methods:
    _ReadRows
    _WriteBuffer
  """

  def __init__(self, table_name, columns):
    """Constructor.

    Args:
      table_name: Name of the table.
      columns: List of unique column names in the table.

    Raises:
      ValueError: If column names are not unique.
    """
    self._table_name = table_name
    # Check if column names are duplicated
    if len(set(columns)) != len(columns):
      raise ValueError("Column names not unique.")
    self._columns = columns
    self._buffer = deque()

  def WriteRow(self, *args, **kwargs):
    """Writes row to storage.

    See _ValidateRow for rules on *args and **kwargs.

    Args:
      args: The row to write, as positional arguments.
      kwargs: The row to write, as keyword arguments.

    Raises:
      ValueError: If the inputs are invalid, or if both args/kwargs are
        specified.
      Error: If the write failed.
    """
    _tmp_buffer = self._buffer
    self.ResetWriteBuffer()
    self.BufferRowForWrite(*args, **kwargs)
    try:
      self.WriteBufferedRows()
    finally:
      self._buffer = _tmp_buffer

  def GetAllRows(self):
    """Return all rows as a list of dicts.

    Returns:
      A list of dicts, with each row's data keyed by the column names.
    """
    return list(self._ReadRows())

  def BufferRowForWrite(self, *args, **kwargs):
    """Buffers rows in memory that should be written.

    See _ConvertInputRow for rules on *args and **kwargs.

    Args:
      args: The row to write, as positional arguments.
      kwargs: The row to write, as keyword arguments.

    Raises:
      ValueError: If the inputs are invalid, or if both args/kwargs are
        specified.
    """
    new_row = self._ConvertInputRow(*args, **kwargs)
    self._BufferRow(new_row)

  def WriteBufferedRows(self):
    """Writes all buffered up rows to storage.

    Raises:
      Error: if the write failed.
    """
    self._WriteBuffer()
    self.ResetWriteBuffer()

  def ResetWriteBuffer(self):
    """Resets the buffer of rows to write."""
    self._buffer = deque()

  def NumBufferedRows(self):
    """Returns number of buffered rows."""
    return len(self._buffer)

  def _ConvertInputRow(self, *args, **kwargs):
    """Converts input row to a validated row dictionary.

    If *args is specified, then they must be coincident with the column names.
    If **kwargs is specified, they must match the column names.
    Both *args and **kwargs cannot be specified.

    Returns:
      The row as a dictionary keyed by the column names.

    Raises:
      ValueError: If input row is invalid.
    """
    if args and kwargs:
      raise ValueError("Only one of *args or **kwargs must be entered.")
    if args:
      if len(args) != len(self._columns):
        raise ValueError(
            "Number of *args does not match with columns: %s" % self._columns)
      row = dict(zip(self._columns, args))
    if kwargs:
      if set(kwargs.keys()) != set(self._columns):
        raise ValueError(
            "Keys in **kwargs does match with columns: %s" % self._columns)
      row = kwargs
    return row

  def _BufferRow(self, row):
    """Add a row to the buffer. Assumes the row has been validated.

    Args:
      row: A dictionary keyed by columns for the row to write.
    """
    self._buffer.append(row)

  def __iter__(self):
    """Allows callers to iterate across rows."""
    return StorageTableIterator(self)

  def _ValidateBuffer(self):
    """Validates that rows in the write buffer is consistent wtih the columns.

    Raises:
      Error: If the rows in the buffer have columns that are inconsistent with
        this object.
    """
    for row in self._buffer:
      if len(self._columns) != len(row.keys()):
        raise Error("Number of cols does not match buffer. Cols: %r, Buffer: %r"
                    % (self._columns, row.keys()))
      if set(self._columns) != set(row.keys()):
        raise Error("Columns do not match buffer. Cols: %r, Buffer: %r"
            % (self._columns, row.keys()))

  def _ReadRows(self):
    """Generator that returns one row at a time.

    THIS METHOD MUST BE OVERRIDDEN BY SUBCLASSES.

    Returns:
      The next row, as a dict keyed by the column names.
    """
    raise NotImplementedError("_ReadRows must be overridden by subclasses.")

  def _WriteBuffer(self):
    """Writes the row buffer to storage. Does NOT clear the write buffer.

    THIS METHOD MUST BE OVERRIDDEN BY SUBCLASSES.

    Raises:
      Error: If the write failed.
    """
    raise NotImplementedError("_WriteBuffer must be overridden by subclasses.")


class StorageTableIterator(StorageTable):
  """Class that enables callers to iterate through rows in StorageTable."""

  def __init__(self, table):
    self._rowgenerator = table._ReadRows()

  def next(self):
    next_row = self._rowgenerator.next()
    if not next_row:
      raise StopIteration
    return next_row


class CsvTable(StorageTable):
  """Subclass that stores rows in a CSV file."""

  file_path = ""

  def __init__(self, csv_config):
    self.file_path = os.path.join(
        os.path.expanduser(FLAGS.csv_base_path), csv_config.rel_path)
    super(CsvTable, self).__init__(
        csv_config.rel_path, csv_config.columns)
    self._rows = self._ReadCsvFile()

  def _ReadRows(self):
    """Generator that returns one row at a time.

    This method overrides the base class method.

    Returns:
      The next row, as a dict keyed by the column names.
    """
    for row in self._rows:
      yield row

  def _WriteBuffer(self):
    """Writes the row buffer to storage, and clears the buffer.

    This method overrides the base class method.

    Raises:
      Error: If the write failed.
    """
    if len(self._buffer) == 0:
      return
    self._ValidateBuffer()
    self._rows += self._buffer
    tmp_path = "{}.tmp".format(self.file_path)
    with open(tmp_path, "w") as f:
      writer = csv.DictWriter(f, fieldnames=self._columns)
      writer.writeheader()
      for row in self._rows:
        writer.writerow(row)
    os.rename(tmp_path, self.file_path)

  def _ReadCsvFile(self):
    """Reads CSV file into memory.

    Returns:
      A list of CSV file rows, keyed by column titles. If the file does not
        exist, an empty list is returned.
    """
    if not os.path.isfile(self.file_path):
      return []
    with open(self.file_path, "r") as f:
      reader = csv.DictReader(f, fieldnames=self._columns)
      # Skip header
      reader.next()
      return list(reader)
