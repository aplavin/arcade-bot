import socket
import struct

# about optimizations in this class: my question http://stackoverflow.com/questions/10742639/faster-sockets-in-python
class Sock():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_buf = b''

    def connect(self):
        self.s.connect(('127.0.0.1', 6666))

    def close(self):
        self.s.close()

    # each time we receive the same known amount of data, so receive it at once
    def recv_prepare(self, cnt):
        self.recv_buf = memoryview(bytearray(cnt))
        cnt_read = 0
        while cnt_read < cnt:
            cnt_read += self.s.recv_into(self.recv_buf[cnt_read:], cnt - cnt_read)

        self.recv_buf_i = 0

    # returns n elements from prepared buffer
    # fmt - format string for ONE element
    # only 4 byte elements supported (e.g. int, float)
    # done for optimization: one call to unpack is faster than many
    # next_* methods use this
    # if possible, call methods which return many values at once
    def next(self, fmt, n):
        fmt = fmt * n
        size = n * 4
        self.recv_buf_i += size
        return struct.unpack_from(fmt, self.recv_buf, offset = self.recv_buf_i - size)

    def next_floats(self, n):
        return self.next('f', n)

    def next_float(self):
        return self.next_floats(1)[0]

    def next_ints(self, n):
        return self.next('i', n)

    def next_int(self):
        return self.next_ints(1)[0]

    # if we don't need next n bytes - skip them
    def skip_read(self, n):
        self.recv_buf_i += n

    # writing NOT OPTIMIZED, because it's not a bottleneck
    def write_int(self, i):
        self.send_buf += struct.pack('i', i)

    def write_float(self, f):
        self.send_buf += struct.pack('f', f)

    def flush(self):
        self.s.sendall(self.send_buf)
        self.send_buf = b''
