from .helpers import MPC5674_Test

ESCI_DEVICES = (
    ('eSCI_A', 0xFFFB0000),
    ('eSCI_B', 0xFFFB4000),
    ('eSCI_C', 0xFFFB8000)
)

#Registers Offests from Base Address
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

#Register's Default Values
ESCI_BRR_DEFAULT_BYTES = b'\x00\x04'
ESCI_BRR_DEFAULT = 0x4
ESCI_CR1_DEFAULT_BYTES = b'\x00\x00'
ESCI_CR1_DEFAULT = 0x0
ESCI_CR2_DEFAULT_BYTES = b'\x20\x00'
ESCI_CR2_DEFAULT = 0x2000
ESCI_CR3_DEFAULT_BYTES = b'\x00\x00'
ESCI_CR3_DEFAULT = 0x00
ESCI_DR_DEFAULT_BYTES = b'\x00\x00'
ESCI_DR_DEFAULT = 0x00
ESCI_IFSR1_DEFAULT_BYTES = b'\x00\x00'
ESCI_IFSR1_DEFAULT = 0x00
ESCI_IFSR2_DEFAULT_BYTES = b'\x00\x00'
ESCI_IFSR2_DEFAULT = 0x00
ESCI_LCR1_DEFAULT_BYTES = b'\x00\x00'
ESCI_LCR1_DEFAULT = 0x00
ESCI_LCR2_DEFAULT_BYTES = b'\x00\x00'
ESCI_LCR2_DEFAULT = 0x00
ESCI_LTR_DEFAULT_BYTES = b'\x00'
ESCI_LTR_DEFAULT = 0x00
ESCI_LRR_DEFAULT_BYTES = b'\x00'
ESCI_LRR_DEFAULT = 0x00
ESCI_LPR_DEFAULT_BYTES = b'\xc5\x99'
ESCI_LPR_DEFAULT = 0xc599


class MPC5674_ESCI(MPC5674_Test):
    
    def test_esci_brr(self):
        for dev in range(len(ESCI_DEVICES)):
            devname, baseaddr = ESCI_DEVICES[dev]
            self.assertEqual(self.emu.sci[dev].devname, devname)
        
            addr = baseaddr + ESCI_BRR_OFFSET
    
            self.assertEqual(self.emu.readMemory(addr, 2), ESCI_BRR_DEFAULT_BYTES)
            self.assertEqual(self.emu.readMemValue(addr, 2), ESCI_BRR_DEFAULT)

            self.assertEqual(self.emu.sci[dev].registers.brr.sbr, 0x4)

            self.emu.writeMemValue(addr, 0xFFFF, 2)
            self.assertEqual(self.emu.readMemValue(addr, 2), 0x1FFF)

    def test_esci_cr1(self):
        for dev in range(len(ESCI_DEVICES)):
            devname, baseaddr = ESCI_DEVICES[dev]
            self.assertEqual(self.emu.sci[dev].devname, devname)
            
            addr = baseaddr + ESCI_CR1_OFFSET
            self.assertEqual(self.emu.readMemory(addr, 2), ESCI_CR1_DEFAULT_BYTES)
            self.assertEqual(self.emu.readMemValue(addr, 2), ESCI_CR1_DEFAULT)

            self.assertEqual(self.emu.sci[dev].registers.cr1.loops, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr1.rsrc, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr1.m, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr1.wake, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr1.ilt, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr1.pe, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr1.pt, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr1.tie, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr1.tcie, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr1.rie, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr1.ilie, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr1.te, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr1.re, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr1.rwu, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr1.sbk, 0x0)

            self.emu.writeMemValue(addr, 0xFFFF, 2)
            self.assertEqual(self.emu.readMemValue(addr, 2), 0xBFFF)

    def test_esci_cr2(self):
        for dev in range(len(ESCI_DEVICES)):
            devname, baseaddr = ESCI_DEVICES[dev]
            self.assertEqual(self.emu.sci[dev].devname, devname)

            addr = baseaddr + ESCI_CR2_OFFSET
            self.assertEqual(self.emu.readMemory(addr, 2), ESCI_CR2_DEFAULT_BYTES)
            self.assertEqual(self.emu.readMemValue(addr, 2), ESCI_CR2_DEFAULT)

            self.assertEqual(self.emu.sci[dev].registers.cr2.mdis, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr2.fbr, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr2.bstp, 0x01)
            self.assertEqual(self.emu.sci[dev].registers.cr2.berrie, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr2.rxdma, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr2.txdma, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr2.brcl, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr2.txdir, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr2.besm, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr2.bestp, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr2.rxpol, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr2.pmsk, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr2.orie, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr2.nfie, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr2.feie, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr2.pfie, 0x0)

            self.emu.writeMemValue(addr, 0xFFFF, 2)
            self.assertEqual(self.emu.readMemValue(addr, 2), 0xFFFF)

    def test_esci_cr3(self):
        for dev in range(len(ESCI_DEVICES)):
            devname, baseaddr = ESCI_DEVICES[dev]
            self.assertEqual(self.emu.sci[dev].devname, devname)

            addr = baseaddr + ESCI_CR3_OFFSET
            self.assertEqual(self.emu.readMemory(addr, 2), ESCI_CR3_DEFAULT_BYTES)
            self.assertEqual(self.emu.readMemValue(addr, 2), ESCI_CR3_DEFAULT)

            self.assertEqual(self.emu.sci[dev].registers.cr3.synm, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr3.eroe, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr3.erfe, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr3.erpe, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.cr3.m2, 0x0)

            self.emu.writeMemValue(addr, 0xFFFF, 2)
            self.assertEqual(self.emu.readMemValue(addr, 2), 0x1F00)

    def test_esci_ifsr1(self):
        for dev in range(len(ESCI_DEVICES)):
            devname, baseaddr = ESCI_DEVICES[dev]
            self.assertEqual(self.emu.sci[dev].devname, devname)

            addr = baseaddr + ESCI_IFSR1_OFFSET
            self.assertEqual(self.emu.readMemory(addr, 2), ESCI_IFSR1_DEFAULT_BYTES)
            self.assertEqual(self.emu.readMemValue(addr, 2), ESCI_IFSR1_DEFAULT)

            self.assertEqual(self.emu.sci[dev].registers.ifsr1.tdre, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr1.tc, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr1.rdrf, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr1.idle, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr1.orun, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr1.nf, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr1.fe, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr1.pf, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr1.berr, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr1.tact, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr1.ract, 0x0)

            self.emu.writeMemValue(addr, 0xFFFF, 2)
            self.assertEqual(self.emu.readMemValue(addr, 2), 0x0000)
            
            self.emu.sci[dev].registers.ifsr1.vsOverrideValue('tdre', 0x1)
            self.emu.sci[dev].registers.ifsr1.vsOverrideValue('tc', 0x1)
            self.emu.sci[dev].registers.ifsr1.vsOverrideValue('rdrf', 0x1)
            self.emu.sci[dev].registers.ifsr1.vsOverrideValue('idle', 0x1)
            self.emu.sci[dev].registers.ifsr1.vsOverrideValue('orun', 0x1)
            self.emu.sci[dev].registers.ifsr1.vsOverrideValue('nf', 0x1)
            self.emu.sci[dev].registers.ifsr1.vsOverrideValue('fe', 0x1)
            self.emu.sci[dev].registers.ifsr1.vsOverrideValue('pf', 0x1)
            self.emu.sci[dev].registers.ifsr1.vsOverrideValue('berr', 0x1)
            self.emu.sci[dev].registers.ifsr1.vsOverrideValue('tact', 0x1)
            self.emu.sci[dev].registers.ifsr1.vsOverrideValue('ract', 0x1)
            self.emu.writeMemValue(addr, 0x0000, 2)
            self.assertEqual(self.emu.readMemValue(addr, 2), 0xFF13)
            self.emu.writeMemValue(addr, 0xFFFF, 2)
            self.assertEqual(self.emu.readMemValue(addr, 2), 0x0003)

    def test_esci_ifsr2(self):
        for dev in range(len(ESCI_DEVICES)):
            devname, baseaddr = ESCI_DEVICES[dev]
            self.assertEqual(self.emu.sci[dev].devname, devname)

            addr = baseaddr + ESCI_IFSR2_OFFSET
            self.assertEqual(self.emu.readMemory(addr, 2), ESCI_IFSR2_DEFAULT_BYTES)
            self.assertEqual(self.emu.readMemValue(addr, 2), ESCI_IFSR2_DEFAULT)

            self.assertEqual(self.emu.sci[dev].registers.ifsr2.rxrdy, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr2.txrdy, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr2.lwake, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr2.sto, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr2.pberr, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr2.cerr, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr2.ckerr, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr2.frc, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr2.ureq, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.ifsr2.ovfl, 0x0)

            self.emu.writeMemValue(addr, 0xFFFF, 2)
            self.assertEqual(self.emu.readMemValue(addr, 2), 0x0000)

            self.emu.sci[dev].registers.ifsr2.vsOverrideValue('rxrdy', 0x1)
            self.emu.sci[dev].registers.ifsr2.vsOverrideValue('txrdy', 0x1)
            self.emu.sci[dev].registers.ifsr2.vsOverrideValue('lwake', 0x1)
            self.emu.sci[dev].registers.ifsr2.vsOverrideValue('sto', 0x1)
            self.emu.sci[dev].registers.ifsr2.vsOverrideValue('pberr', 0x1)
            self.emu.sci[dev].registers.ifsr2.vsOverrideValue('cerr', 0x1)
            self.emu.sci[dev].registers.ifsr2.vsOverrideValue('ckerr', 0x1)
            self.emu.sci[dev].registers.ifsr2.vsOverrideValue('frc', 0x1)
            self.emu.sci[dev].registers.ifsr2.vsOverrideValue('ureq', 0x1)
            self.emu.sci[dev].registers.ifsr2.vsOverrideValue('ovfl', 0x1)
            self.emu.writeMemValue(addr, 0x0000, 2)
            self.assertEqual(self.emu.readMemValue(addr, 2), 0xFF03)
            self.emu.writeMemValue(addr, 0xFFFF, 2)
            self.assertEqual(self.emu.readMemValue(addr, 2), 0x0000)



    def test_esci_lcr1(self):
        for dev in range(len(ESCI_DEVICES)):
            devname, baseaddr = ESCI_DEVICES[dev]
            self.assertEqual(self.emu.sci[dev].devname, devname)

            addr = baseaddr + ESCI_LCR1_OFFSET
            self.assertEqual(self.emu.readMemory(addr, 2), ESCI_LCR1_DEFAULT_BYTES)
            self.assertEqual(self.emu.readMemValue(addr, 2), ESCI_LCR1_DEFAULT)

            self.assertEqual(self.emu.sci[dev].registers.lcr1.lres, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.lcr1.wu, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.lcr1.wud, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.lcr1.prty, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.lcr1.lin, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.lcr1.rxie, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.lcr1.txie, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.lcr1.wuie, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.lcr1.stie, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.lcr1.pbie, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.lcr1.cie, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.lcr1.ckie, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.lcr1.fcie, 0x0)

            self.emu.writeMemValue(addr, 0xFFFF, 2)
            self.assertEqual(self.emu.readMemValue(addr, 2), 0xF3FF)

    def test_esci_lcr2(self):
        for dev in range(len(ESCI_DEVICES)):
            devname, baseaddr = ESCI_DEVICES[dev]
            self.assertEqual(self.emu.sci[dev].devname, devname)

            addr = baseaddr + ESCI_LCR2_OFFSET
            self.assertEqual(self.emu.readMemory(addr, 2), ESCI_LCR2_DEFAULT_BYTES)
            self.assertEqual(self.emu.readMemValue(addr, 2), ESCI_LCR2_DEFAULT)

            self.assertEqual(self.emu.sci[dev].registers.lcr2.uqie, 0x0)
            self.assertEqual(self.emu.sci[dev].registers.lcr2.ofie, 0x0)

            self.emu.writeMemValue(addr, 0xFFFF, 2)
            self.assertEqual(self.emu.readMemValue(addr, 2), 0x0300)

    def test_esci_lrr(self):
        for dev in range(len(ESCI_DEVICES)):
            devname, baseaddr = ESCI_DEVICES[dev]
            self.assertEqual(self.emu.sci[dev].devname, devname)

            addr = baseaddr + ESCI_LRR_OFFSET
            self.assertEqual(self.emu.readMemory(addr, 1), ESCI_LRR_DEFAULT_BYTES)
            self.assertEqual(self.emu.readMemValue(addr, 1), ESCI_LRR_DEFAULT)


            self.assertEqual(self.emu.sci[dev].registers.lrr.d, 0x0)
            
            self.emu.writeMemValue(addr, 0xFF, 1)
            self.assertEqual(self.emu.readMemValue(addr, 1), 0x00)

    def test_esci_lpr(self):
        for dev in range(len(ESCI_DEVICES)):
            devname, baseaddr = ESCI_DEVICES[dev]
            self.assertEqual(self.emu.sci[dev].devname, devname)

            addr = baseaddr + ESCI_LPR_OFFSET
            self.assertEqual(self.emu.readMemory(addr, 2), ESCI_LPR_DEFAULT_BYTES)
            self.assertEqual(self.emu.readMemValue(addr, 2), ESCI_LPR_DEFAULT)

            self.assertEqual(self.emu.sci[dev].registers.lpr.p, 0xc599)
            
            self.emu.writeMemValue(addr, 0xFFFF, 2)
            self.assertEqual(self.emu.readMemValue(addr, 2), 0xFFFF)

    def test_undefined_offsets(self):
        self.validate_invalid_read(0xFFFB001C, 4)
        self.validate_invalid_read(0xFFFB0011, 1)
        self.validate_invalid_read(0xFFFB0012, 2)
        self.validate_invalid_read(0xFFFB0015, 1)
        self.validate_invalid_read(0xFFFB0016, 2)
