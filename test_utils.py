"""Utilities for unit testing."""


import storage_lib


class FakeStorageTable(storage_lib.StorageTable):
  """Fake storage class used for testing."""

  _fake_rows = []

  def __init__(self, table_name, columns, **kwargs):
    super(FakeStorageTable, self).__init__(table_name, columns)
    if "fake_rows" in kwargs.keys():
      self._fake_rows = kwargs["fake_rows"]
    else:
      self._fake_rows = []

  def _ReadRows(self):
    for row in self._fake_rows:
      yield row

  def _WriteBuffer(self):
    self._fake_rows += self._buffer
    self._buffer = []
