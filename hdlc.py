#!/usr/bin/env python3

class HDLCBaseFrame:
    """
    A basic HDLC frame with all common data fields. All other frame classes
    derive from this.
    """

    _address = None
    _control = None
    _fcs = None
    def __init__(self):
        _address = bytes(1)   # 0,8 or 16 bits, depending on data link
        _control = bytes(1)   # 8 or 16 bits
        _fcs = bytes(2)       # 16 or 32 bits frame check sequence

    # address handling
    def parse_address(self, rawchunk, addresslength=1):
        """
        Extract the address out of a given serial data chunk.
        The input is expected to be an instance bytes(), since
        Byte arrays can be modified while being parsed. The address
        length is assumed to be 8 bits (1 byte) by default.
        """
        if not isinstance(rawchunk,bytes):
            raise TypeError("no bytes-object given")

        stripped = True
        if (126 == rawchunk[0]) and (126 == rawchunk[-1]):
                stripped = False

        if not (126 == rawchunk[0]) and (126 == rawchunk[-1]):
                raise ValueError("opening flag corrupt / not 0x7e")

        if (126 == rawchunk[0]) and not (126 == rawchunk[-1]):
                raise ValueError("closing flag corrupt / not 0x7e")

        # minimal: no data field
        if (not stripped and len(rawchunk) <= 5) or (stripped and len(rawchunk) <= 3):
            raise ValueError("to few bytes given")

        # check address
        if not isinstance(addresslength,int):
            raise TypeError("address length of wrong type, only int allowed")
        if 0 > addresslength:
            raise ValueError("given address length too short")
        if 2 < addresslength:
            raise ValueError("given address length too big")
