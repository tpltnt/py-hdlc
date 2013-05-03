from GenericFrame import GenericFrame

class IFrame(GenericFrame):
    """
    A HDLC I-Frame implementation

    .. todo::

    * r/w all parts of control field

    """

    def __init__(self):
        super().__init__()

    def get_receive_sequence_number(self):
        """
        Extract transmit receive sequence number from control field.

        :returns: int -- receive sequence number
        :raises: ValueError

        """
        if 1 == len(self._GenericFrame__control):
            # 8 bit control field
            ctrlbits = self._GenericFrame__control[0]
            # masking up to (expected) 8 bits
            if 8 < ctrlbits.bit_length():
                raise ValueError("internal control field longer than 8 bits")
            # mask out all but lowest (rightmost) 3 bits
            mask = ~0xf8
            seqbits = ctrlbits & mask
            return int(seqbits)
        else:
            # 16 bit control field
            raise NotImplementedError("handling 16bit control fields not implemented (yet)")
