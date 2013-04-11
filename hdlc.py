#!/usr/bin/env python3

class HDLCBaseFrame:
    """
    A basic HDLC frame with all common data fields. All other frame classes
    derive from this.
    """

    _adress = None
    def __init__(self):
        _adress = \x00

