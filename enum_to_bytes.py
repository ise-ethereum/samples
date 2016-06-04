from Chess import *
import binascii


def enum_to_bytes(enum):
    decimals = []
    for e in enum:
        decimals.append(e.value)
    bytes_hex = "".join('\\x%s' % format(n, 'x').zfill(2) for n in decimals)
    return decimals, bytes_hex


print('Flags:\n%s\n%s' % enum_to_bytes(Flags))
print('Direction:\n%s\n%s' % enum_to_bytes(Direction))
print('Piece:\n%s\n%s' % enum_to_bytes(Piece))
