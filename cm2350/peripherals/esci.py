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
        #This bit along with RSCR need special handling.
        self.loops = v_bits(1)
        self._pad1 = v_const(1)
        #This bit along with loops need special handling.
        self.rsrc = v_bits(1)
        #This sets start and stop bits for frames. I dont believe this is needed since we wont
        self.m = v_bits(1)
        #I believe ther will be no sleep, so no wake needeD?
        self.wake = v_bits(1)
        #Needs special handling - only to throw exception that sleep / wake is not a supported feature.
        self.ilt = v_bits(1)
        #no frames so no parity biuts needed?
        self.pe = v_bits(1)
        #again, no frames no parity?
        self.pt = v_bits(1)
        #Interrupt not needed per erin
        self.tie = v_bits(1)
        #Interrupt not needed per erin
        self.tcie = v_bits(1)
        #Interrup not needed per erin
        self.rie = v_bits(1)
        #Interrupt not needed per erin
        self.ilie = v_bits(1)
        #Interrupt not needed per erin
        self.te = v_bits(1)
        #Special handling Needed to determine  if enabled then process message, if disabled, ignore it.
        self.re = v_bits(1)
        #no wakeup mode will be in place, not needed?
        self.rwu = v_bits(1)
        #This sends determines if a break character is set. I dont believe we will need to have a break charcater ever to denote end of stream and return to ready state mode?
        self.sbk = v_bits(1)

#Haoppy with how this one looks.
class ESCI_x_CR2(PeriphRegister):
    def __init__(self):
        super().__init__()
        #Needs special handling, if enabled, process message, if disabled ignore.
        self.mdis = v_bits(1)
        #This is transmission error detection. This looks like layer 2 err checking and thus not needeD?
        self.fbr = v_bits(1)
        #Review with Erin, I didnt get DMA
        self.bstp = v_bits(1, 0b1)
        #This bit controls the BERR interrupt request generation, but is not hte interrupt itself. Review with Erin, how to handle this?
        self.berrie = v_bits(1)
        #Probably needs special handling
        self.rxdma = v_bits(1)
        #Probvably needs special handling
        self.txdma = v_bits(1)
        #Break Character length, I dont believe we need break characters?
        self.brcl = v_bits(1)
        #This enabled / disabled the TXD pin. layer 1 stuff not needed?
        self.txdir = v_bits(1)
        #This is fast bit err detection. Sounds like layer 2 stuff not needed?
        self.besm = v_bits(1)
        #Interrupt not needed per erin
        self.bestp = v_bits(1)
        #Pin Polarity?! have Erinr eview with me, but I dont believe it is needed
        self.rxpol = v_bits(1)
        #Parity bit masking. parity bits not used/ therefore this not needed
        self.pmsk = v_bits(1)
        #Interrupt not needed per erin
        self.orie = v_bits(1)
        #Interrupt not needed per erin
        self.nfie = v_bits(1)
        #Interrupt not needed per erin
        self.feie = v_bits(1)
        #Interrupt not needed per erin
        self.pfie = v_bits(1)
        #Interrupt not needed per erin

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
        self.pf  = v_w1c(1)
        #pad remains pad
        self._pad1  = v_const(3)
        #renamed from berr to bestp for interrupt processing
        self.bestp  = v_w1c(1)
        #pad remains pad
        self._pad2  = v_const(2)
        #Transmitter active, status bit is set as long as transmmittion of frame is active. Likely dont need special handling.
        self.tact  = v_const(1)
        #Receiver active, bit set during reception of data. likely wont need special handling?
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
        #Will require special handling. Lin enginer in operation / idle
        self.lres  = v_bits(1)
        #LIN wake up trigger, not needed as no wake up
        self.wu  = v_bits(1)
        #LIN wake up delimiter time, not needeed no wake up
        self.wud  = v_bits(2)
        #pad remains pad
        self._pad1  = v_const(2)
        #controls 2x parity bits in LIN header, not neede since no headers
        self.prty  = v_bits(1)
        #needs special handling. 0 = sci mode, 1 = LIN mode
        self.lin  = v_bits(1)
        #this looks a LOT like a normal interrupt. Run apst erin why it is not in the interrupt table
        self.rxie  = v_bits(1)
        #This looks a lot lieka normal interrupt, ask erin why not in interrupt table
        self.txie  = v_bits(1)
        #Wakeup interrupt bit, no wake up, not needed
        self.wuie  = v_bits(1)
        #ask erin why this is not in interrupt table
        self.stie  = v_bits(1)
        #ask erin why this is not in interrupt table
        self.pbie  = v_bits(1)
        ##ask erin why this is not in interrupt table
        self.cie  = v_bits(1)
        ##ask erin why this is not in interrupt table
        self.ckie  = v_bits(1)
        #ask erin why this is not in interrupt table
        self.fcie  = v_bits(1)

#Happy with how this one looks
class ESCI_x_LCR2(PeriphRegister):
    def __init__(self):
        super().__init__()
        self._pad1 = v_const(6)
        #ask erin why this is not in interrupt table
        self.uqie = v_bits(1)
        #ask erin why this is not in interrupt table
        self.ofie  = v_bits(1)
        #pad remains pad
        self._pad2  = v_const(8)

#Ummm this one is confusing. Wait for Erin
class ESCI_x_LTR(PeriphRegister):
    def __init__(self):
        super().__init__()
        #whole register will require special handling
        self.filler = v_bits(8)

#Happy with hose this looks?
class ESCI_x_LRR(PeriphRegister):
    def __init__(self):
        super().__init__()
        #whole register will require special handling
        self.d   = v_const(8)

#happy with how this looks.
class ESCI_x_LPR(PeriphRegister):
    def __init__(self):
        super().__init__()
        #no descrion or details on this?
        self.p  = v_bits(16, 0b1100010110011001)

class ESCI_x_CR3(PeriphRegister):
    def __init__(self):
        super().__init__()
        self._pad1 = v_const(3)
        #Syncronization sequence not needed?
        self.synm = v_bits(1)
        #noty sure about overruns
        self.eroe = v_bits(1)
        #not sure
        self.erfe = v_bits(1)
        #Probably not needed, double check
        self.erpe = v_bits(1)
        #will require special handling
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
            'bestp':    INTC_EVENT.ESCIA_IFSR1_BERR,        
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
            'bestp':    INTC_EVENT.ESCIB_IFSR1_BERR,    
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
            'bestp':    INTC_EVENT.ESCIC_IFSR1_BERR,    
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


class eSCI(ExternalIOPeripheral):
    def __init__(self, devname, emu, mmio_addr):
        super().__init__(emu, devname, mmio_addr, 0x4000, regsetcls=ESCI_REGISTERS, 
                #isrstatus=('ifsr1','ifsr2'), isrflags=('cr1','cr2'), isrevents=ESCI_INT_EVENTS)
                isrstatus='ifsr1', isrflags='cr1', isrevents=ESCI_INT_EVENTS)




















