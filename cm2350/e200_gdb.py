import sys
import time
import signal
import logging
import threading

import envi
import envi.archs.ppc.regs as eapr
import vtrace.platforms.gdbstub as vtp_gdb

from . import mmio
from . import intc_exc
from .gdbdefs import e200z759n3

logger = logging.getLogger(__name__)


__all__ = [
    'e200GDB',
]


# TODO: handle reset
# TODO: handle monitor commands (monitor reset)


STATE_DISCONNECTED = 0
STATE_CONNECTED = 1
STATE_RUNNING = 2
STATE_PAUSED = 3


# the DNH instruction opcodes for BookE and VLE modes, the instructions are 
# organized first by a flag indicating if the instruction should be VLE, and 
# secondly by size
PPC_DNH_INSTR_BYTES = {
    0: {
        4: b'\x4c\x00\x01\x8c',
    },
    1: {
        2: b'\x00\x0F',
        4: b'\x7c\x00\x00\xc2',
    },
}


class e200GDB(vtp_gdb.GdbBaseEmuServer):
    '''
    Emulated hardware debugger/gdb-stub for the e200 core.
    '''
    def __init__(self, emu):
        # TODO: figure out GPR 32/64 bit stuff, same for PC/LR/CTR, and all SPRs
        # such as specifying TBL vs TB.
        #reggrps = [
        #    ('general',     'org.gnu.gdb.power.core'),
        #    ('spe',         'org.gnu.gdb.power.spe'),
        #    ('spr',         'org.gnu.gdb.power.spr'),
        #]
        #vtp_gdb.GdbBaseEmuServer.__init__(self, emu, reggrps=reggrps)
        vtp_gdb.GdbBaseEmuServer.__init__(self, emu)

        emu.modules['GDBSTUB'] = self

        # To track breakpoints, for the purposes of emulation both hardware and 
        # software breakpoints are treated the same
        self._bpdata = {}
        self._bps_in_place = False

        # There is no real filename for the firmware image
        self.xfer_read_handlers[b'exec-file'] = None

        # We don't support the vfile handlers for this debug connection
        self.vfile_handlers = {}

    def getTargetXml(self, reggrps):
        # Hardcoded register format and XML
        self._gdb_reg_fmt = e200z759n3.reg_fmt
        self._gdb_target_xml = e200z759n3.target_xml

        self._updateEnviGdbIdxMap()

    def initProcessInfo(self):
        self.pid = 1

    def waitForClient(self):
        while self.connstate != vtp_gdb.STATE_CONN_CONNECTED:
            time.sleep(0.1)

    def isClientConnected(self):
        return self.connstate == vtp_gdb.STATE_CONN_CONNECTED

    def init(self, emu):
        logger.info("e200GDB Initialized.")

        if self.runthread is None:
            logger.info("starting GDBServer runthread")
            self.runthread = threading.Thread(target=self.runServer, daemon=True)
            self.runthread.start()
        else:
            logger.critical("WTFO!  self.runthread is not None?")

    def handleInterrupts(self, interrupt):
        # TODO: emulate the PPC debug control registers that can disable/enable 
        # some things?

        # If there is a debugger connected halt execution, otherwise queue the 
        # debug exception so it can be processed by the normal PPC exception 
        # handler.
        if self.isClientConnected():
            self.emu._do_halt()
            self._pullUpBreakpoints()
        else:
            self.emu.queueException(interrupt)

    def _postClientAttach(self, addr):
        # TODO: Install callbacks for signals that should cause execution to 
        # halt.

        logger.info("Client attached: %r", repr(addr))
        logger.info("Halting processor")
        self._halt_reason = signal.SIGTRAP
        self.emu.halt_exec()

    def _serverBreak(self):
        self._halt_reason = signal.SIGTRAP
        self.emu.halt_exec()
        return self._halt_reason

    def _serverCont(self):
        # If the program counter is at a breakpoint execute the current 
        # (original) instruction before restoring the breakpoints
        if self.emu.getProgramCounter() in self._bpdata:
            # The breakpoints should not be installed because we are halted
            assert not self._bps_in_place

            # Should have no problem doing stepi in the server thread because 
            # the primary thread should be halted.
            self._serverStepi()

        # Restore the breakpoints and resume execution
        self._putDownBreakpoints()

        # Continue execution
        self._halt_reason = 0
        self.emu.resume_exec()

        # TODO also check _serverBREAK and _handleBREAK

        return self._halt_reason

    def _installBreakpoint(self, addr):
        ea, vle, _, _, breakbytes, breakop = self._bpdata[addr]

        with self.emu.getAdminRights():
            self.emu.writeOpcode(addr, breakbytes)

        self.emu.updateOpcache(ea, vle, breakop)

    def _uninstallBreakpoint(self, addr):
        ea, vle, origbytes, origop, _, _ = self._bpdata[addr]

        with self.emu.getAdminRights():
            self.emu.writeOpcode(addr, origbytes)

        self.emu.updateOpcache(ea, vle, origop)

    def _putDownBreakpoints(self):
        '''
        At each emulator stop, we want to replace the original bytes.  On 
        resume, we put the Break instruction bytes back in.
        '''
        if not self._bps_in_place:
            logger.debug('Installing breakpoints: ' + ','.join(hex(a) for a in self._bpdata))
            for va in self._bpdata:
                self._installBreakpoint(va)
            self._bps_in_place = True

    def _pullUpBreakpoints(self):
        '''
        At each emulator stop, we want to replace the original bytes.  On 
        resume, we put the Break instruction bytes back in.
        '''
        if self._bps_in_place:
            logger.debug('Removing breakpoints: ' + ','.join(hex(a) for a in self._bpdata))
            for va in self._bpdata:
                self._uninstallBreakpoint(va)
            self._bps_in_place = False

    def _serverSetSWBreak(self, addr):
        return self._serverSetHWBreak(addr)

    def _serverSetHWBreak(self, addr):
        if addr in self._bpdata:
            raise Exception('Cannot add breakpoint that already exists @ 0x%x' % addr)

        logger.debug('Adding new breakpoint: 0x%x' % addr)
        origbytes = self._bpdata.get(addr)
        if origbytes:
            # Error, this breakpoint is already set
            return b'E02'

        try:
            # Find the opcode being replaced
            op = self.emu.parseOpcode(addr, skipcallbacks=True)

        except intc_exc.MceDataReadBusError:
            return b'E%02d' % signal.SIGSEGV

        except intc_exc.DataTlbException:
            return b'E%02d' % signal.SIGBUS

        # Get the break instruction info
        ea, vle, origop, origbytes = self.emu.getInstrInfo(addr, skipcache=True)

        # Create a new break instruction for the target address
        breakbytes = PPC_DNH_INSTR_BYTES[vle][origop.size]

        # Generate the breakpoint instruction object for the target address
        if vle:
            breakop = self.emu._arch_vle_dis.disasm(breakbytes, 0, addr)
        else:
            breakop = self.emu._arch_dis.disasm(breakbytes, 0, addr)

        # Save the physical address, vle flag, original bytes, original 
        # instruction, breakpoint bytes, and breakpoint instruction we just 
        # created.
        self._bpdata[addr] = (ea, vle, origbytes, origop, breakbytes, breakop)

        # If breakpoints are currently installed, add the new one.
        if self._bps_in_place:
            self._installBreakpoint(addr)

        return b'OK'

    def _serverRemoveSWBreak(self, addr):
        return self._serverRemoveHWBreak(addr)

    def _serverRemoveHWBreak(self, addr):
        if addr not in self._bpdata:
            raise Exception('Cannot remove breakpoint that doesn\'t exist @ 0x%x' % addr)

        # Only need to write the original data back to memory if the breakpoint 
        # is currently in memory.
        logger.debug('Removing breakpoint: 0x%x' % addr)
        if self._bps_in_place:
            self._uninstallBreakpoint(addr)
        del self._bpdata[addr]

        return b'OK'

    def _serverDetach(self):
        vtp_gdb.GdbBaseEmuServer._serverDetach(self)

        # Clear all breakpoints and resume execution
        self._pullUpBreakpoints()
        self._bpdata = {}
        self._bps_in_place = False

        # Signal to the emulator that the gdb client has detached
        self.emu.debug_client_detached()

    def _serverQSymbol(self, cmd_data):
        # we have no symbol information
        return b'OK'

    def getMemoryMapXml(self):
        self._gdb_memory_map_xml = b'''<?xml version="1.0" ?>
<!DOCTYPE memory-map
  PUBLIC '+//IDN gnu.org//DTD GDB Memory Map V1.0//EN'
  'http://sourceware.org/gdb/gdb-memory-map.dtd'>
<memory-map>
  <memory length="0xafc000" start="0x400000" type="ram"/>
  <memory length="0xfc000" start="0xf00000" type="ram"/>
  <memory length="0xff000000" start="0x1000000" type="ram"/>
  <memory length="0x400000" start="0x0" type="flash">
    <property name="blocksize">0x800</property>
  </memory>
  <memory length="0x4000" start="0xefc000" type="flash">
    <property name="blocksize">0x800</property>
  </memory>
  <memory length="0x4000" start="0xffc000" type="flash">
    <property name="blocksize">0x800</property>
  </memory>
</memory-map>
'''

    def _serverReadMem(self, addr, size):
        # The particular error msg doesn't matter, but for testing purposes use 
        # the signal numbers to indicate the type of failure:
        #   - MMU error         = SIGBUS
        #   - unable to read    = SIGSEGV
        try:
            return vtp_gdb.GdbBaseEmuServer._serverReadMem(self, addr, size)

        except intc_exc.MceDataReadBusError:
            #return b'E%02d' % signal.SIGSEGV

            # We have to just accept this or GDB gets really weird
            return b'00000000'

        except intc_exc.DataTlbException:
            #return b'E%02d' % signal.SIGBUS

            # We have to just accept this or GDB gets really weird
            return b'00000000'

    def _serverWriteMem(self, addr, val):
        # The particular error msg doesn't matter, but for testing purposes use 
        # the signal numbers to indicate the type of failure:
        #   - MMU error         = SIGBUS
        #   - unable to write   = SIGSEGV

        try:
            return vtp_gdb.GdbBaseEmuServer._serverWriteMem(self, addr, val)

        except intc_exc.MceDataWriteBusError:
            #return b'E%02d' % signal.SIGSEGV

            # We have to just accept this or GDB gets really weird
            return b'OK'

        except intc_exc.DataTlbException:
            #return b'E%02d' % signal.SIGBUS

            # We have to just accept this or GDB gets really weird
            return b'OK'

