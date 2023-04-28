from .helpers import MPC5674_Test

class MPC5674_ESCI(MPC5674_Test):
    def test_ESCI(self):
        self.assertEqual(self.emu.readMemValue(0xFFFB0000,2),0b0000000000000100)
        self.assertEqual(self.emu.readMemValue(0xFFFB0002,2),0b0000000000000000)
        self.assertEqual(self.emu.readMemValue(0xFFFB0004,2),0b0010000000000000)
#        self.assertEqual(self.emu.readMemValue(0xFFFB0006,2),0b0000000000000000)
        self.assertEqual(self.emu.readMemValue(0xFFFB0008,2),0b0000000000000000)
        self.assertEqual(self.emu.readMemValue(0xFFFB000a,2),0b0000000000000000)
        self.assertEqual(self.emu.readMemValue(0xFFFB000c,2),0b0000000000000000)
        self.assertEqual(self.emu.readMemValue(0xFFFB000e,2),0b0000000000000000)
#        self.assertEqual(self.emu.readMemValue(0xFFFB0010,1),0b00000000)
        self.assertEqual(self.emu.readMemValue(0xFFFB0014,1),0b00000000)
        self.assertEqual(self.emu.readMemValue(0xFFFB0018,2),0b1100010110011001)
        self.assertEqual(self.emu.readMemValue(0xFFFB001a,2),0b0000000000000000)
    
    def test_undefined_offsets(self):
        self.validate_invalid_read(0xFFFB001C, 4)
        self.validate_invalid_read(0xFFFB0011, 1)
        self.validate_invalid_read(0xFFFB0012, 2)
        self.validate_invalid_read(0xFFFB0015, 1)
        self.validate_invalid_read(0xFFFB0016, 2)
    
    def test_attempt_write(self):
        self.emu.writeMemValue(0xFFFB0000, 0b1111111111111111, 2)
        self.assertEqual(self.emu.readMemValue(0xFFFB0000,2),0b0001111111111111)

        self.emu.writeMemValue(0xFFFB0000, 0b1111111111111111, 2)
        self.emu.writeMemValue(0xFFFB0000, 0b1111111111111111, 2)
        self.emu.writeMemValue(0xFFFB0000, 0b1111111111111111, 2)
        self.emu.writeMemValue(0xFFFB0000, 0b1111111111111111, 2)
        self.emu.writeMemValue(0xFFFB0000, 0b1111111111111111, 2)
        self.emu.writeMemValue(0xFFFB0000, 0b1111111111111111, 2)
        self.emu.writeMemValue(0xFFFB0000, 0b1111111111111111, 2)
        self.emu.writeMemValue(0xFFFB0000, 0b1111111111111111, 2)
