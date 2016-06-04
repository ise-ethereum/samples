from Chess import *
import binascii


def list_to_bytes(values, offset=0):
    bytes_hex = "".join('\\x%s' % format(n+offset, 'x').zfill(2) for n in values)
    return values, bytes_hex


def enum_to_bytes(enum, offset=0):
    """
    Convert enum values to a byte string.
    Can optionally offset values to handle negative cases
    """
    values = []
    for e in enum:
        values.append(e.value)
    return list_to_bytes(values, offset)


print('Flags:\n%s\n%s' % enum_to_bytes(Flags))
print('Direction:\n%s\n%s' % enum_to_bytes(Direction, offset=64))
print('Piece:\n%s\n%s' % enum_to_bytes(Piece, offset=64))
knight_moves = [-33, -31, -18, -14, 14, 18, 31, 33];
print('Knight moves:\n%s\n%s' % list_to_bytes(knight_moves, offset=64))
