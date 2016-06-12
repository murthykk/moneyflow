"""Set of classes tha handle data storage."""


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

  def WriteBufferedRows(self, *args, **kwargs):
    """Writes all buffered up rows to storage."""
    raise NotImplementedError

  def ValidateRow(*args, **kwargs):
    # TODO

  def _ReadRows(self):
    """Inner generator."""
    raise NotImplementedError


class CsvStorage(Storage):
  def __init__(self, csv_config):
    self._file_path = csv_config.GetFilePath()
    super(CsvStorage, self).__init__(
        csv_config.GetCsvName(), csv_config.GetColumns())
    # TODO: Read the entire file into memory

  def BufferRowForWrite(self, *args, **kwargs):
    """Buffers up rows in memory that should be written."""
    raise NotImplementedError

  def WriteBufferedRows(self, *args, **kwargs):
    """Writes all buffered up rows to storage."""
    raise NotImplementedError

  def _ReadRows(self):
    """Generator that returns rows from the CSV."""
