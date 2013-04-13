#!/usr/bin/env python3

class HDLCBaseFrame:
    """
    A basic HDLC frame with all common data fields. All other frame classes
    derive from this.
    """

    _adress = None
    _control = None
    _fcs = None # frame check sequence
    def __init__(self):
        _adress = bytes(1)    # 8+ bits
        _control = bytes(1)   # 8 or 16 bits
        _fcs = bytes(2)       # 16 or 32 bits

