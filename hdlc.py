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
    def parse_address(self, rawchunk, stripped=True):
        """
        Extract the address out of a given serial data chunk.
        The input is expected to be an instance bytes(), since
        Byte arrays can be modified while being parsed.

        Arguments:
        - rawchunk: raw serial data chunk as bytes()
        - stripped: True indicates that the flag-segment (0x7e) is stripped from the given rawchunk. False indicates that the flag segment is still contianed
        """
        if not isinstance(rawchunk,bytes):
            raise TypeError("no bytes-object given")
        if (not stripped and 4 <= len(rawchunk) ) or (2 <= len(rawchunk)):
            raise ValueError("to few bytes given")

