"""Set of classes tha handle data storage."""

import json
import gflags as flags


STORAGE_TYPES = ["csv"]


flags.DEFINE_enum(
    "storage_type", "csv", STORAGE_TYPES, "Type of backend storage to use.")
flags.DEFINE_string(
    "storage_config_file", "storage_config.json",
    "Base directory where all CSVs will be stored.")
flags.DEFINE_string(
    "csv_base_dir", "csvdata", "Base directory where all CSVs will be stored.")


FLAGS = flags.FLAGS


def GetStorageObject(storage_name):
  """Returns a storage interface object, given a storage config object."""
  config = StorageConfig.fromconfigfile(FLAGS.storage_config_file, storage_name)
  if FLAGS.storage_type == "csv":
    return CsvStorage(config)


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


class Storage(object):
  """Storage base class."""
  def __init__(self, table_name, columns):
    self._table_name = table_name
    self._columns = columns
    self._buffer = []

  def WriteRow(self, *args, **kwargs):
    pass

  def GetAllRows(self):
    """Return all rows as a list of dicts."""

  def BufferRowForWrite(self, *args, **kwargs):
    """Buffers up rows in memory that should be written."""
    raise NotImplementedError

  def WriteBufferedRows(self):
    """Writes all buffered up rows to storage."""
    raise NotImplementedError

  def ValidateRow(*args, **kwargs):
    # TODO
    pass

  def __iter__(self):
    return self

  def next(self):
    for row in self._ReadRows():
      yield row

  def _ReadRows(self):
    """Inner generator."""
    raise NotImplementedError


class CsvStorage(Storage):
  def __init__(self, csv_config):
    self._file_path = csv_config.rel_path
    super(CsvStorage, self).__init__(
        csv_config.rel_path, csv_config.columns)
    # TODO: Read the entire file into memory

  def BufferRowForWrite(self, *args, **kwargs):
    """Buffers up rows in memory that should be written."""
    raise NotImplementedError

  def WriteBufferedRows(self):
    """Writes all buffered up rows to storage."""
    raise NotImplementedError

  def _ReadRows(self):
    """Generator that returns rows from the CSV."""
