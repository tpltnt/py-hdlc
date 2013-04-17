#!/usr/bin/env python3

class HDLCBaseFrame(object):
    """
    A basic HDLC frame with all common data fields. All other frame classes
    derive from this.
    """

    __address = None
    __control = None
    __fcs = None
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
        SDLC uses 8bit addresses, SS7 doesn't use the address field
        at all.
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
        if (not stripped and len(rawchunk) <= 4) or (stripped and len(rawchunk) <= 2):
            raise ValueError("to few bytes given")

        # strip given chunk for easier parsing
        __parsechunk = rawchunk
        if not stripped:
            byteslist = [rawchunk[i] for i in range(1,len(rawchunk)-1)]
            __parsechunk = bytes(byteslist)

        # check address
        if not isinstance(addresslength,int):
            raise TypeError("address length of wrong type, only int allowed")
        if 0 > addresslength:
            raise ValueError("given address length too short")
        if 2 < addresslength:
            raise ValueError("given address length too big")
        if 1 == addresslength:
            self.__address = bytes([__parsechunk[0]])
        if 1 < addresslength and 127 <= __parsechunk[0]:
            raise ValueError("")


    def is_broadcast(self):
        """Simple self-test for being a broadcast frame. It may only be
        used with a command frame."""

        if None == self._HDLCBaseFrame__address:
            return False

        if (len(self._HDLCBaseFrame__address) == 1) and (255 == self._HDLCBaseFrame__address[0]):
            return True
        else:
            return False


    def set_address(self,address):
        """This method sets the address field. In the basic format, only
        8bit addresses are allowed."""
        if no instance(address,bytes):
            raise TypeError("given address has to be of type bytes")
