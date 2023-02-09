import struct

def decode(blob):
    return struct.unpack("f" * 1536, blob)

def encode(values):
    return struct.pack("f" * 1536, *values)