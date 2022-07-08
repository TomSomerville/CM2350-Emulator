from ..ppc_vstructs import *
from ..ppc_peripherals import *

import logging
logger = logging.getLogger(__name__)

__all__ = [
    'PIT',
]


class PIT(MMIOPeripheral):
    def __init__(self, emu, mmio_addr):
        super().__init__(emu, 'PIT', mmio_addr, 0x4000)

    def _getPeriphReg(self, offset, size):
        # return placeholder data
        return b'\x00' * size

    def _setPeriphReg(self, offset, data):
        # Do nothing
        pass
