#Copied Imports from dspi.py - please review

import enum

import envi.bits as e_bits

from ..ppc_vstructs import *
from ..ppc_peripherals import *
from ..intc_exc import INTC_EVENT

import logging
logger = logging.getLogger(__name__)

#__all__ = [
#    'eSCI',
#]

ESCI_BRR_OFFSET     = 0x0000

ESCI_CR1_OFFSET    = 0x0002
ESCI_CR2_OFFSET    = 0x0004
ESCI_CR3_OFFSET    = 0x001A

ESCI_DR_OFFSET    = 0x0006

ESCI_IFSR1_OFFSET    = 0x0008
ESCI_IFSR2_OFFSET    = 0x000A

ESCI_LCR1_OFFSET    = 0x000C
ESCI_LCR2_OFFSET    = 0x000E

ESCI_LTR_OFFSET    = 0x0010
ESCI_LRR_OFFSET    = 0x0014
ESCI_LPR_OFFSET    = 0x0018


#Happy with how this one looks
class ESCI_x_BRR(PeriphRegister):
    def __init__(self):
        super().__init__()
        self._pad1 = v_const(3, 0b000)
        self.sbr = v_bits(13, 0b0000000000100)

#This register has horizontal split for the RWU bit space also shares with rwm.
class ESCI_x_CR1(PeriphRegister):
    def __init__(self):
        super().__init__()
        self.loops = v_bits(1)
        self._pad1 = v_const(1)
        self.rsrc = v_bits(1)
        self.m = v_bits(1)
        self.wake = v_bits(1)
        self.ilt = v_bits(1)
        self.pe = v_bits(1)
        self.pt = v_bits(1)
        self.tie = v_bits(1)
        self.tcie = v_bits(1)
        self.rie = v_bits(1)
        self.ilie = v_bits(1)
        self.te = v_bits(1)
        self.re = v_bits(1)
        self.rwu = v_bits(1)
        self.sbk = v_bits(1)

#Haoppy with how this one looks.
class ESCI_x_CR2(PeriphRegister):
    def __init__(self):
        super().__init__()
        self.mdis = v_bits(1)
        self.fbr = v_bits(1)
        self.bstp = v_bits(1, 0b1)
        self.berrie = v_bits(1)
        self.rxdma = v_bits(1)
        self.txdma = v_bits(1)
        self.brcl = v_bits(1)
        self.txdir = v_bits(1)
        self.besm = v_bits(1)
        self.bestp = v_bits(1)
        self.rxpol = v_bits(1)
        self.pmsk = v_bits(1)
        self.orie = v_bits(1)
        self.nfie = v_bits(1)
        self.feie = v_bits(1)
        self.pfie = v_bits(1)

#This register has the horizontal split fgor RD/TD. needs more work
class ESCI_x_DR(PeriphRegister):
    def __init__(self):
        super().__init__()
        self.rn  = v_const(1)
        self.tn  = v_bits(1)
        self.err = v_const(1)
        self._pad1  = v_const(1)
        self.rd1  = v_const(4)
        self.rdtd1  = v_bits(1)
        self.rdtd2  = v_bits(7)


#this register has the horizontal split thing where verything is w1c on bottom
class ESCI_x_IFSR1(PeriphRegister):
    def __init__(self):
        super().__init__()
        self.tdre  = v_w1c(1)
        self.tc  = v_w1c(1)
        self.rdrf  = v_w1c(1)
        self.idle  = v_w1c(1)
        self.orun  = v_w1c(1)
        self.nf  = v_w1c(1)
        self.fe  = v_w1c(1)
        self.pf  = v_w1c(1)
        self._pad1  = v_const(3)
        self.berr  = v_w1c(1)
        self._pad2  = v_const(2)
        self.tact  = v_const(1)
        self.ract  = v_const(1)

#All of these have the horizontal split. needs more work.
class ESCI_x_IFSR2(PeriphRegister):
    def __init__(self):
        super().__init__()
        self.rxrdy  = v_w1c(1)
        self.txrdy  = v_w1c(1)
        self.lwake  = v_w1c(1)
        self.sto  = v_w1c(1)
        self.pberr  = v_w1c(1)
        self.cerr  = v_w1c(1)
        self.ckerr  = v_w1c(1)
        self.frc  = v_w1c(1)
        self._pad1  = v_const(6)
        self.ureq  = v_w1c(1)
        self.ovfl  = v_w1c(1)

#this one has the horizontal split for the wu register. needs more work
class ESCI_x_LCR1(PeriphRegister):
    def __init__(self):
        super().__init__()
        self.lres  = v_bits(1)
        self.wu  = v_bits(1)
        self.wud  = v_bits(2)
        self._pad1  = v_const(2)
        self.prty  = v_bits(1)
        self.lin  = v_bits(1)
        self.rxie  = v_bits(1)
        self.txie  = v_bits(1)
        self.wuie  = v_bits(1)
        self.stie  = v_bits(1)
        self.pbie  = v_bits(1)
        self.cie  = v_bits(1)
        self.ckie  = v_bits(1)
        self.fcie  = v_bits(1)

#Happy with how this one looks
class ESCI_x_LCR2(PeriphRegister):
    def __init__(self):
        super().__init__()
        self._pad1 = v_const(6)
        self.uqie = v_bits(1)
        self.ofie  = v_bits(1)
        self._pad2  = v_const(8)

#Ummm this one is confusing. Wait for Erin
class ESCI_x_LTR(PeriphRegister):
    def __init__(self):
        super().__init__()
        self.filler = v_bits(8)

#Happy with hose this looks?
class ESCI_x_LRR(PeriphRegister):
    def __init__(self):
        super().__init__()
        self.d   = v_const(8)

#happy with how this looks.
class ESCI_x_LPR(PeriphRegister):
    def __init__(self):
        super().__init__()
        self.p  = v_bits(16, 0b1100010110011001)

class ESCI_x_CR3(PeriphRegister):
    def __init__(self):
        super().__init__()
        self._pad1 = v_const(3)
        self.synm = v_bits(1)
        self.eroe = v_bits(1)
        self.erfe = v_bits(1)
        self.erpe = v_bits(1)
        self.m2 = v_bits(1)
        self._pad2 = v_const(8)


class ESCI_REGISTERS(PeripheralRegisterSet):
    def __init__(self):
        super().__init__()

        self.brr = (ESCI_BRR_OFFSET, ESCI_x_BRR())
        self.cr1 = (ESCI_CR1_OFFSET, ESCI_x_CR1())
        self.cr2 = (ESCI_CR2_OFFSET, ESCI_x_CR2()) 
        self.cr3 = (ESCI_CR3_OFFSET, ESCI_x_CR3()) 
        self.ifsr1 = (ESCI_IFSR1_OFFSET, ESCI_x_IFSR1())
        self.ifsr2 = (ESCI_IFSR2_OFFSET, ESCI_x_IFSR2())
        self.lcr1 = (ESCI_LCR1_OFFSET, ESCI_x_LCR1())
        self.lcr2 = (ESCI_LCR2_OFFSET, ESCI_x_LCR2()) 
        self.lrr = (ESCI_LRR_OFFSET, ESCI_x_LRR())  
        self.lpr = (ESCI_LPR_OFFSET, ESCI_x_LPR())

class eSCI(ExternalIOPeripheral):
    def __init__(self, devname, emu, mmio_addr):
        super().__init__(emu, devname, mmio_addr, 0x4000, regsetcls=ESCI_REGISTERS)

