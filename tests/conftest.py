import sys
sys.path.append('../py-hdlc')
import pytest
from hdlc import HDLCBaseFrame


@pytest.fixture(scope="module")
def baseframe():
    return HDLCBaseFrame()
