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
ESCI_BRR_SIZE       = 2
ESCI_BRR_RANGE      = range(ESCI_BRR_OFFSET, ESCI_BRR_OFFSET + ESCI_BRR_SIZE)
ESCI_CR1_OFFSET     = 0x0002
ESCI_CR1_SIZE       = 2
ESCI_CR1_RANGE      = range(ESCI_CR1_OFFSET, ESCI_CR1_OFFSET + ESCI_CR1_SIZE)
ESCI_CR2_OFFSET     = 0x0004
ESCI_CR2_SIZE       = 2
ESCI_CR2_RANGE      = range(ESCI_CR2_OFFSET, ESCI_CR2_OFFSET + ESCI_CR2_SIZE)
ESCI_CR3_OFFSET     = 0x001A
ESCI_CR3_SIZE       = 2
ESCI_CR3_RANGE      = range(ESCI_CR3_OFFSET, ESCI_CR3_OFFSET + ESCI_CR3_SIZE)

ESCI_DR_OFFSET      = 0x0006
ESCI_DR_SIZE        = 2
ESCI_DR_RANGE       = range(ESCI_DR_OFFSET, ESCI_DR_OFFSET + ESCI_DR_SIZE)

ESCI_IFSR1_OFFSET   = 0x0008
ESCI_IFSR1_SIZE     = 2
ESCI_IFSR1_RANGE    = range(ESCI_IFSR1_OFFSET, ESCI_IFSR1_OFFSET + ESCI_IFSR1_SIZE)
ESCI_IFSR2_OFFSET   = 0x000A
ESCI_IFSR2_SIZE     = 2
ESCI_IFSR2_RANGE    = range(ESCI_IFSR2_OFFSET, ESCI_IFSR2_OFFSET + ESCI_IFSR2_SIZE)

ESCI_LCR1_OFFSET    = 0x000C
ESCI_LCR1_SIZE      = 2
ESCI_LCR1_RANGE     = range(ESCI_LCR1_OFFSET, ESCI_LCR1_OFFSET + ESCI_LCR1_SIZE)
ESCI_LCR2_OFFSET    = 0x000E
ESCI_LCR2_SIZE      = 2
ESCI_LCR2_RANGE     = range(ESCI_LCR2_OFFSET, ESCI_LCR2_OFFSET + ESCI_LCR2_SIZE)

ESCI_LTR_OFFSET     = 0x0010
ESCI_LTR_SIZE       = 1
ESCI_LTR_RANGE      = range(ESCI_LTR_OFFSET, ESCI_LTR_OFFSET + ESCI_LTR_SIZE)
ESCI_LRR_OFFSET     = 0x0014
ESCI_LRR_SIZE       = 1
ESCI_LRR_RANGE      = range(ESCI_LRR_OFFSET, ESCI_LRR_OFFSET + ESCI_LRR_SIZE)
ESCI_LPR_OFFSET     = 0x0018
ESCI_LPR_SIZE       = 2
ESCI_LPR_RANGE      = range(ESCI_LPR_OFFSET, ESCI_LPR_OFFSET + ESCI_LPR_SIZE)


#No Fancy Dancy Needed
class ESCI_x_BRR(PeriphRegister):
    def __init__(self):
        super().__init__()
        self._pad1 = v_const(3, 0b000)
        #Needs special handling for the isntance of lower byte written two without preceding byte, if upper byte has a non zero value.
        self.sbr = v_bits(13, 0b0000000000100)


class ESCI_x_CR1(PeriphRegister):
    def __init__(self):
        super().__init__()
        #Special Handling Completed Via vsAddParseCallback in __init__
        self.loops = v_bits(1)
        self._pad1 = v_const(1)
        #Special Handling Completed Via vsAddParseCallback in __init__
        self.rsrc = v_bits(1)
        #No Special Handling Needed
        self.m = v_bits(1)
        #No SpecialHandling Needed
        self.wake = v_bits(1)
        #Special Handling Completed Via vsAddParseCallback in __init__
        self.ilt = v_bits(1)
        #No SpecialHandling Needed
        self.pe = v_bits(1)
        #No SpecialHandling Needed
        self.pt = v_bits(1)
        #No SpecialHandling Needed
        self.tie = v_bits(1)
        #No SpecialHandling Needed
        self.tcie = v_bits(1)
        #No SpecialHandling Needed
        self.rie = v_bits(1)
        #No SpecialHandling Needed
        self.ilie = v_bits(1)
        #No SpecialHandling Needed
        self.te = v_bits(1)
        #Special Handling Completed Via vsAddParseCallback in __init__
        self.re = v_bits(1)
        #No SpecialHandling Needed
        self.rwu = v_bits(1)
        #Special Handling Completed Via vsAddParseCallback in __init__
        self.re = v_bits(1)
        #Special Handling Completed Via vsAddParseCallback in __init__
        self.sbk = v_bits(1)

#Haoppy with how this one looks.
class ESCI_x_CR2(PeriphRegister):
    def __init__(self):
        super().__init__()
        #Special Handling Completed Via vsAddParseCallback in __init__
        self.mdis = v_bits(1)

        #No SpecialHandling Needed
        self.fbr = v_bits(1)

        #No SpecialHandling Needed
        self.bstp = v_bits(1, 0b1)

        #No SpecialHandling Needed
        self.berrie = v_bits(1)

        #Ignore for now - Will need special Sauce Probably needs special handling
        self.rxdma = v_bits(1)

        #Ignore for now - Will need special Sauce Probvably needs special handling
        self.txdma = v_bits(1)

        #No SpecialHandling Needed
        self.brcl = v_bits(1)

        #No SpecialHandling Needed
        self.txdir = v_bits(1)

        #No SpecialHandling Needed
        self.besm = v_bits(1)

        #No SpecialHandling Needed
        self.bestp = v_bits(1)

        #No SpecialHandling Needed
        self.rxpol = v_bits(1)

        #Special Handling Completed Via vsAddParseCallback in __init__
        self.pmsk = v_bits(1)

        #Interrupt not needed per erin
        self.orie = v_bits(1)

        #Interrupt not needed per erin
        self.nfie = v_bits(1)

        #Interrupt not needed per erin
        self.feie = v_bits(1)

        #Interrupt not needed per erin
        self.pfie = v_bits(1)

#This register has the horizontal split fgor RD/TD. needs more work
class ESCI_x_DR(PeriphRegister):
    def __init__(self):
        super().__init__()
        #This entire register will need special handling
        self.rn  = v_const(1)
        self.tn  = v_bits(1)
        self.err = v_const(1)
        self._pad1  = v_const(1)
        self.rd1  = v_const(4)
        self.rdtd1  = v_bits(1)
        self.rdtd2  = v_bits(7)


class ESCI_x_IFSR1(PeriphRegister):
    def __init__(self):
        super().__init__()
        #Renamed from tdre to tie for interrupt processing
        self.tie  = v_w1c(1)
        #renamed from tc to tcie for interrupt processing
        self.tcie  = v_w1c(1)
        #renamed from rdrf to rie for interrupt processing
        self.rie  = v_w1c(1)
        #renamed from idle to ilie (L) for interrupt processing
        self.ilie  = v_w1c(1)
        #renamed from orun to orie for interrupt processing
        self.orie  = v_w1c(1)
        #renamed from nf to nfie for interrupt processing
        self.nfie  = v_w1c(1)
        #renamed from fe to feie for interrupt processing
        self.feie  = v_w1c(1)
        #renamed from pf to pfie for interrupt processing
        self.pfie  = v_w1c(1)
        #pad remains pad
        self._pad1  = v_const(3)
        #renamed from berr to bestp for interrupt processing
        self.bestp  = v_w1c(1)
        #pad remains pad
        self._pad2  = v_const(2)
        #No SpecialHandling Needed
        self.tact  = v_const(1)
        #No SpecialHandling Needed
        self.ract  = v_const(1)

class ESCI_x_IFSR2(PeriphRegister):
    def __init__(self):
        super().__init__()
        #Renamed from rxrdy to rxie for interrupt processing
        self.rxie = v_w1c(1)
        #renamed from txrdy to txie for interrupt processing
        self.txie  = v_w1c(1)
        #renamed from lwake to wuie for interrupt processing
        self.wuie = v_w1c(1)
        #renamed from sto to stie for interrupt processing
        self.stie  = v_w1c(1)
        #renamed from pberr to pbie for interrupt processing
        self.pbie  = v_w1c(1)
        #renamed from cerr to cie for interrupt processing
        self.cie  = v_w1c(1)
        #renamed from ckerr to ckie for interrupt processing
        self.ckie  = v_w1c(1)
        #renamed from frc to fcie for interrupt processing
        self.fcie  = v_w1c(1)
        #pad remains pad
        self._pad1  = v_const(6)
        #renamed from ureq to uqie for interrupt processing
        self.uqie  = v_w1c(1)
        #renamed from ovfl to ofie for interrupt processing
        self.ofie  = v_w1c(1)

class ESCI_x_LCR1(PeriphRegister):
    def __init__(self):
        super().__init__()
        #Special Handling Completed Via vsAddParseCallback in __init__
        self.lres  = v_bits(1)

        #No SpecialHandling Needed
        self.wu  = v_bits(1)

        #No SpecialHandling Needed
        self.wud  = v_bits(2)

        #pad remains pad
        self._pad1  = v_const(2)

        #No SpecialHandling Needed
        self.prty  = v_bits(1)

        #Special Handling Completed Via vsAddParseCallback in __init__
        self.lin  = v_bits(1)

        #Interrupt not needed per erin
        self.rxie  = v_bits(1)

        #Interrupt not needed per erin
        self.txie  = v_bits(1)

        #No SpecialHandling Needed
        self.wuie  = v_bits(1)

        #Interrupt not needed per erin
        self.stie  = v_bits(1)

        #Interrupt not needed per erin
        self.pbie  = v_bits(1)

        #Interrupt not needed per erin
        self.cie  = v_bits(1)

        #Interrupt not needed per erin
        self.ckie  = v_bits(1)

        #Interrupt not needed per erin
        self.fcie  = v_bits(1)

#Happy with how this one looks
class ESCI_x_LCR2(PeriphRegister):
    def __init__(self):
        super().__init__()
        #pad remains pad
        self._pad1 = v_const(6)

        #Interrupt not needed per erin
        self.uqie = v_bits(1)

        #Interrupt not needed per erin
        self.ofie  = v_bits(1)

        #pad remains pad
        self._pad2  = v_const(8)

#Ummm this one is confusing. Wait for Erin
class ESCI_x_LTR(PeriphRegister):
    def __init__(self):
        super().__init__()
        #whole register will require special handling. Raise exception if CRC Enable bit is set.
        self.filler = v_bits(8)

#Happy with hose this looks?
class ESCI_x_LRR(PeriphRegister):
    def __init__(self):
        super().__init__()
        #whole register will require special handling
        self.d   = v_const(8)

class ESCI_x_LPR(PeriphRegister):
    def __init__(self):
        super().__init__()
        #No SpecialHandling Needed
        self.p  = v_bits(16, 0b1100010110011001)

class ESCI_x_CR3(PeriphRegister):
    def __init__(self):
        super().__init__()
        #pad remains pad
        self._pad1 = v_const(3)

        #No SpecialHandling Needed
        self.synm = v_bits(1)

        #No SpecialHandling Needed
        self.eroe = v_bits(1)

        #No SpecialHandling Needed
        self.erfe = v_bits(1)

        #No SpecialHandling Needed
        self.erpe = v_bits(1)

        #No SpecialHandling Needed
        self.m2 = v_bits(1)

        #pad remains pad
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

ESCI_INT_EVENTS = {
        'ESCI_A': {
            'tie':      INTC_EVENT.ESCIA_IFSR1_TDRE,
            'tcie':     INTC_EVENT.ESCIA_IFSR1_TC,
            'rie':      INTC_EVENT.ESCIA_IFSR1_RDRF,
            'ilie':     INTC_EVENT.ESCIA_IFSR1_IDLE,
            'orie':     INTC_EVENT.ESCIA_IFSR1_OR,
            'nfie':     INTC_EVENT.ESCIA_IFSR1_NF,
            'feie':     INTC_EVENT.ESCIA_IFSR1_FE,
            'pfie':     INTC_EVENT.ESCIA_IFSR1_PF,
            'berrie':    INTC_EVENT.ESCIA_IFSR1_BERR,
            #'rxie':     INTC_EVENT.ESCIA_IFSR2_RXRDY,
            #'txie':     INTC_EVENT.ESCIA_IFSR2_TXRDY,
            #'wuie':     INTC_EVENT.ESCIA_IFSR2_LWAKE,
            #'stie':     INTC_EVENT.ESCIA_IFSR2_STO,
            #'pbie':     INTC_EVENT.ESCIA_IFSR2_PBERR,
            #'cie':      INTC_EVENT.ESCIA_IFSR2_CERR,
            #'ckie':     INTC_EVENT.ESCIA_IFSR2_CKERR,
            #'fcie':     INTC_EVENT.ESCIA_IFSR2_FRC,
            #'ofie':     INTC_EVENT.ESCIA_IFSR2_OVFL,
            #'uqie':     INTC_EVENT.ESCIA_IFSR2_UREQ
        },
        'ESCI_B': {
            'tie':      INTC_EVENT.ESCIB_IFSR1_TDRE,
            'tcie':     INTC_EVENT.ESCIB_IFSR1_TC,
            'rie':      INTC_EVENT.ESCIB_IFSR1_RDRF,
            'ilie':     INTC_EVENT.ESCIB_IFSR1_IDLE,
            'orie':     INTC_EVENT.ESCIB_IFSR1_OR,
            'nfie':     INTC_EVENT.ESCIB_IFSR1_NF,
            'feie':     INTC_EVENT.ESCIB_IFSR1_FE,
            'pfie':     INTC_EVENT.ESCIB_IFSR1_PF,
            'berrie':    INTC_EVENT.ESCIB_IFSR1_BERR,
            #'rxie':     INTC_EVENT.ESCIB_IFSR2_RXRDY,
            #'txie':     INTC_EVENT.ESCIB_IFSR2_TXRDY,
            #'wuie':     INTC_EVENT.ESCIB_IFSR2_LWAKE,
            #'stie':     INTC_EVENT.ESCIB_IFSR2_STO,
            #'pbie':     INTC_EVENT.ESCIB_IFSR2_PBERR,
            #'cie':      INTC_EVENT.ESCIB_IFSR2_CERR,
            #'ckie':     INTC_EVENT.ESCIB_IFSR2_CKERR,
            #'fcie':     INTC_EVENT.ESCIB_IFSR2_FRC,
            #'ofie':     INTC_EVENT.ESCIB_IFSR2_OVFL,
            #'uqie':     INTC_EVENT.ESCIB_IFSR2_UREQ
        },
        'ESCI_C': {
            'tie':      INTC_EVENT.ESCIC_IFSR1_TDRE,
            'tcie':     INTC_EVENT.ESCIC_IFSR1_TC,
            'rie':      INTC_EVENT.ESCIC_IFSR1_RDRF,
            'ilie':     INTC_EVENT.ESCIC_IFSR1_IDLE,
            'orie':     INTC_EVENT.ESCIC_IFSR1_OR,
            'nfie':     INTC_EVENT.ESCIC_IFSR1_NF,
            'feie':     INTC_EVENT.ESCIC_IFSR1_FE,
            'pfie':     INTC_EVENT.ESCIC_IFSR1_PF,
            'berrie':    INTC_EVENT.ESCIC_IFSR1_BERR,
            #'rxie':     INTC_EVENT.ESCIC_IFSR2_RXRDY,
            #'txie':     INTC_EVENT.ESCIC_IFSR2_TXRDY,
            #'wuie':     INTC_EVENT.ESCIC_IFSR2_LWAKE,
            #'stie':     INTC_EVENT.ESCIC_IFSR2_STO,
            #'pbie':     INTC_EVENT.ESCIC_IFSR2_PBERR,
            #'cie':      INTC_EVENT.ESCIC_IFSR2_CERR,
            #'ckie':     INTC_EVENT.ESCIC_IFSR2_CKERR,
            #'fcie':     INTC_EVENT.ESCIC_IFSR2_FRC,
            #'ofie':     INTC_EVENT.ESCIC_IFSR2_OVFL,
            #'uqie':     INTC_EVENT.ESCIC_IFSR2_UREQ
        }
}


class RECEIVER_SOURCE_MODE(enum.IntEnum):

    DUALWIRE    = 0
    LOOP        = 2
    SINGLEWIRE  = 3

class RECEIVER_STATE(enum.IntEnum):

    DISABLED    = 0
    ENABLED     = 1

class MODULE_MODE_OF_OPERATION(enum.IntEnum):

    DISABLED    = 0
    ENABLED     = 1

class PARITY_BIT_MASKING(enum.IntEnum):

    DISABLED    = 0
    ENABLED     = 1

class LIN_PROTOCOL_ENGINE_RESET(enum.IntEnum):

    OPERATIONAL = 0
    IDLE        = 1

class LIN_SCI_MODE(enum.IntEnum):

    SCI         = 0
    LIN         = 1

class eSCI(ExternalIOPeripheral):
    def __init__(self, devname, emu, mmio_addr):
        super().__init__(emu, devname, mmio_addr, 0x4000, regsetcls=ESCI_REGISTERS,
                #isrstatus=('ifsr1','ifsr2'), isrflags=('cr1','cr2'), isrevents=ESCI_INT_EVENTS)
                isrstatus='ifsr1', isrflags='cr1', isrevents=ESCI_INT_EVENTS)

        self.registers.cr1.vsAddParseCallback('loops', self.setReceiverSourceMode)
        self.registers.cr1.vsAddParseCallback('rscr', self.setReceiverSourceMode)
        self.registers.cr1.vsAddParseCallback('ilt', self.wakeNotSupported)
        self.registers.cr1.vsAddParseCallback('re', self.setReceiverEnabled)
        self.registers.cr1.vsAddParseCallback('sbk', self.breakCharacterNotSupported)
        self.registers.cr2.vsAddParseCallback('mdis', self.moduleModeOfOperation)
        self.registers.cr2.vsAddParseCallback('pmsk', self.parityBitMasking)
        self.registers.cr2.vsAddParseCallback('lres', self.linProtocolEngineReset)
        self.registers.cr2.vsAddParseCallback('lin', self.linModeControl)

    def linModeControl(self, thing):
        if self.registers.cr2.lin == 0:
            self.mode = LIN_SCI_MODE.SCI
        if self.registers.cr2.lin == 1:
            self.mode = LIN_SCI_MODE.LIN

    def linProtocolEngineReset(self, thing):
        if self.registers.cr2.lres == 0:
            self.linProtoEnginer = LIN_PROTOCOL_ENGINE_RESET.OPERATIONAL
        elif self.registers.cr2.lres == 1:
            self.linProtoEnginer = LIN_PROTOCOL_ENGINE_RESET.IDLE

    def parityBitMasking(self, thing):
        if self.registers.cr2.pmsk == 0:
            self.parityBitMask = PARITY_BIT_MASKING.DISABLE
        elif self.registers.cr2.pmsk == 1:
            self.parityBitMask = PARITY_BIT_MASKING.ENABLE

    def moduleModeOfOperation(self, thing):
        if self.registers.cr2.mdis == 0:
            self.moduleModeOfOperation = MODULE_MODE_OF_OPERATION.DISABLE
        elif self.registers.cr2.mdis == 1:
            self.moduleModeOfOperation = MODULE_MODE_OF_OPERATION.ENABLE

    def breakCharacterNotSupported(self, thing):
        raise NotImplementedError("Setting/Sending of break characters not implimented yet.")

    def setReceiverEnabled(self, thing):
        if self.registers.cr1.re == 0:
            self.receiverEnable = RECEIVER_STATE.DISABLED
        elif self.registers.cr1.re == 1:
            self.receiverEnable = RECEIVER_STATE.ENABLED

    def wakeNotSupported(self, thing):
        #no idea what thing is, but appears as an arg in all parsecallbacks
        raise NotImplementedError("Idle/Sleep/Wake Not yet Supported")

    def setReceiverSourceMode(self, thing):
        #no idea what thing is, but appears as an arg in all parsecallbacks
        if self.registers.cr1.loops == 1 and self.registers.cr1.rscr == 1:
            self.receiverSourceMode = RECEIVER_SOURCE_MODE.SINGLEWIRE
        elif self.registers.cr1.loops == 1 and self.registers.cr1.rscr == 0:
            self.receiverSourceMode = RECEIVER_SOURCE_MODE.LOOP
        elif self.registers.cr1.loops == 0 and self.registers.cr1.rscr == 0:
            self.receiverSourceMode = RECEIVER_SOURCE_MODE.DUALWIRE

    def reset(self, emu):
        super().reset(emu)
        self.brrShadowReg = 0
        self.receiverEnable = 0
        self.receiverSourceMode = 0
        self.moduleModeOfOperation = 0
        self.parityBitMask = 0
        self.linProtoEngine = 0
        self.mode = 0

    def _setPeriphReg(self, offset, bytez):

        if offset in ESCI_BRR_RANGE:
            if len(bytez) == 2:
                self.registers.brr.sbr = e_bits.parsebytes(bytez, 0, 2, bigend=self.emu.getEndian())
                self.brrShadowReg = 0
            elif offset == ESCI_BRR_OFFSET:
                self.brrShadowReg = bytez[0]
            elif offset == ESCI_BRR_OFFSET + 1:
                self.registers.brr.sbr = (self.brrShadowReg << 8) | bytez[0]
                self.brrShadowReg = 0
        elif offset in ESCI_DR_RANGE:
            #In LIN mode, all write access is ignored
            pass
        elif offset in ESCI_LTR_RANGE:
            pass
        elif offset in ESCI_LRR_RANGE:
            pass
        #elif offsett in ESCI_REG2_RANGE:
        #   pass
        else:
            super()._setPeriphReg(offset, bytez)



    def _get_PeriphReg(self, offset, bytez):

        if offset in ESCI_DR_RANGE:
            #If LIN access is enabled return all 0's
            pass
        else:
            super()._getPeriphReg(offset, bytez)














