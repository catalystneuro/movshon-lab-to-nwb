"""
Original classes and functions taken from: https://mworks.github.io/documentation/latest/reference/event_file_format/index.html

Edited: 
30/06/2021 - Luiz Tauffer 
    - get_events_by_name() function makes SQL query of events by name
    - get_events_by_code() function makes SQL query of events by code
    - decode() function unpacks byte data
    - get_event_names() functions returns list with all events names
"""
from __future__ import division, print_function, unicode_literals
import pandas as pd
import struct
import sqlite3
import zlib
import msgpack

buffer = bytes


class LDOError(Exception):
    pass


class LDOReader(object):

    MAGIC = b'\x89CBF\x01\x00\x00'

    INTEGER_N =  0x02
    INTEGER_P =  0x03
    OPAQUE =     0x0A
    NULL =       0x0B
    LIST =       0x0C
    DICTIONARY = 0x0D
    FLOAT =      0x11

    def __init__(self, file, string_encoding='utf-8'):
        magic = file.read(len(self.MAGIC))
        if not isinstance(magic, type(b'')):
            raise TypeError('file.read() must return binary data')
        if magic != self.MAGIC:
            raise LDOError('invalid magic')

        def _read(size):
            assert size > 0
            data = file.read(size)
            if not data:
                raise EOFError
            return data
        self._read = _read

        self._readers = {
            self.INTEGER_N: self._read_integer_n,
            self.INTEGER_P: self._read_integer_p,
            self.OPAQUE: self._read_opaque,
            self.NULL: self._read_null,
            self.LIST: self._read_list,
            self.DICTIONARY: self._read_dict,
            self.FLOAT: self._read_float,
            }

        self.string_encoding = string_encoding

    def _read_ord(self):
        return ord(self._read(1))

    def _read_ber(self):
        # Adapted from https://stackoverflow.com/questions/6776553/
        value = 0
        while True:
            tmp = self._read_ord()
            value = (value << 7) | (tmp & 0x7f)
            if tmp & 0x80 == 0:
                return value

    def _read_integer_n(self):
        return -(self._read_ber())

    def _read_integer_p(self):
        return self._read_ber()

    def _read_opaque(self):
        size = self._read_ber()
        value = self._read(size)

        # If value contains exactly one NUL, and that NUL is the last
        # byte in the array, then value is an encoded string.  Strip
        # the NUL and decode with the specified encoding.
        if value.find(b'\0') == len(value) - 1:
            value = value[:-1].decode(self.string_encoding)

        return value

    def _read_null(self):
        return None

    def _read_list(self):
        size = self._read_ber()
        return list(self.read() for _ in range(size))

    def _read_dict(self):
        size = self._read_ber()
        return dict((self.read(), self.read()) for _ in range(size))

    def _read_float(self):
        size = self._read_ber()  # Should always be 8
        return struct.unpack(b'<d', self._read(size))[0]

    def read(self):
        typecode = self._read_ord()
        try:
            return self._readers[typecode]()
        except KeyError:
            raise LDOError('invalid type code (0x%0.2X)' % typecode)


class MWKReader(object):

    def __init__(self, filename):
        self._fp = open(filename, 'rb')

    def close(self):
        self._fp.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def __iter__(self):
        self._fp.seek(0)
        reader = LDOReader(self._fp)
        while True:
            try:
                event = reader.read()
                assert isinstance(event, list)
                assert len(event) in (2, 3)
                if len(event) == 2:
                    event.append(None)
                yield event
            except EOFError:
                break


class MWK2Reader(object):

    _compressed_text_type_code = 1
    _compressed_msgpack_stream_type_code = 2

    def __init__(self, filename):
        self._conn = sqlite3.connect(filename)
        self._unpacker = msgpack.Unpacker(raw=False, strict_map_key=False)

        # Get mapping of code/event name
        df = self.get_events_by_code(event_code=0)
        d = df.data[0]
        self.name_to_code = dict((d[c]['tagname'].replace('#', ''), c) for c in d)

    def close(self):
        self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    @staticmethod
    def _decompress(data):
        return zlib.decompress(data, -15)

    def __iter__(self):
        for code, time, data in self._conn.execute('SELECT * FROM events'):
            if not isinstance(data, buffer):
                yield (code, time, data)
            else:
                try:
                    obj = msgpack.unpackb(data, raw=False)
                except msgpack.ExtraData:
                    # Multiple values, so not valid compressed data
                    pass
                else:
                    if isinstance(obj, msgpack.ExtType):
                        if obj.code == self._compressed_text_type_code:
                            yield (code,
                                   time,
                                   self._decompress(obj.data).decode('utf-8'))
                            continue
                        elif (obj.code ==
                              self._compressed_msgpack_stream_type_code):
                            data = self._decompress(obj.data)
                self._unpacker.feed(data)
                try:
                    while True:
                        yield (code, time, self._unpacker.unpack())
                except msgpack.OutOfData:
                    pass

    def decode(self, data):
        if not isinstance(data, buffer):
            return data
        else:
            try:
                obj = msgpack.unpackb(data, raw=False)
            except msgpack.ExtraData:
                # Multiple values, so not valid compressed data
                pass
            else:
                if isinstance(obj, msgpack.ExtType):
                    if obj.code == self._compressed_text_type_code:
                        return self._decompress(obj.data).decode('utf-8')
                    elif obj.code == self._compressed_msgpack_stream_type_code:
                        data = self._decompress(obj.data)
            self._unpacker.feed(data)
            try:
                while True:
                    return self._unpacker.unpack()
            except msgpack.OutOfData:
                pass

    def get_events_by_code(self, event_code):
        """Get dataframe containing all occurrences of specified event."""
        query = f"""
            SELECT time, data
            FROM events
            WHERE code={event_code};
        """
        df = pd.read_sql_query(query, self._conn)
        df['data'] = df['data'].apply(self.decode)
        return df

    def get_events_by_name(self, event_name):
        """Get dataframe containing all occurrences of specified event."""
        code = self.name_to_code[event_name]
        query = f"""
            SELECT time, data
            FROM events
            WHERE code={code};
        """
        df = pd.read_sql_query(query, self._conn)
        df['data'] = df['data'].apply(self.decode)
        return df

    def get_event_names(self):
        """Returns list with all event names"""
        return list(self.name_to_code.keys())