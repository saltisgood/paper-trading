class CircularBufferAdaptor:
    def __init__(self, l: list):
        self._buffer = l
        self._buffer_len = len(self._buffer)

    def __getitem__(self, index: int):
        return self._buffer[self._get_index(index)]

    def _get_index(self, index: int):
        return index % self._buffer_len

    def from_offset(self, offset: int):
        for i in range(self._buffer_len):
            yield self[i + offset]
