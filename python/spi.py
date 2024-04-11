#
# spi.py
# Software SPI for rxafsk.py
# 
# This implementation is for personal experiments.
# Copyright (c) 2024 Tsuyoshi Ohashi
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php
#

import pigpio
from rxafskconst import *

#debug flag primitive
_debug = False  #True

class Spi:
        # configure raspi pins
        # I/O and SOFTWARE SPI
        def __init__(self):
            self.pi = pigpio.pi()
            if not self.pi.connected:
                raise Exception("Error: pigpio NOT connected")
            # pin configuration
            # nCS pin
            self.pi.set_mode(GPIO_nCS, pigpio.OUTPUT)
            self.pi.write(GPIO_nCS, 1)  # nCS = 1
            # MOSI pin
            self.pi.set_mode(GPIO_MOSI, pigpio.OUTPUT)
            self.pi.write(GPIO_MOSI, 0)  # MOSI = 0
            # MISO pin
            self.pi.set_mode(GPIO_MISO, pigpio.INPUT)
            self.pi.set_pull_up_down(GPIO_MISO, pigpio.PUD_DOWN) # pull down
            # SCLK pin
            self.pi.set_mode(GPIO_SCLK, pigpio.OUTPUT)
            self.pi.write(GPIO_SCLK, 0)  # SCLK = 0

            # nRTS pin
            self.pi.set_mode(GPIO_nRTS, pigpio.OUTPUT)
            self.pi.write(GPIO_nRTS, 1)  # PIN_nRTS = High
            # nRESET pin
            self.pi.set_mode(GPIO_nRESET, pigpio.OUTPUT)
            self.pi.write(GPIO_nRESET, 1)  # PIN_nRESET = High
            
            # CD pin  
            self.pi.set_mode(GPIO_CD, pigpio.INPUT)
            self.pi.set_pull_up_down(GPIO_CD, pigpio.PUD_DOWN) # pull down

            # CNVST pin
            self.pi.set_mode(GPIO_CNVST, pigpio.OUTPUT)
            self.pi.write(GPIO_CNVST, 0)  # PIN_CNVST = Low
            
        # primitive 
        # Set nCS pin Low
        def _select(self):
            if(_debug):
                print("\t_select")
            self.pi.write(GPIO_nCS, 0)
        # Set nCS pin High
        def _deselect(self):
            if(_debug):
                print("\t_deselect")
            self.pi.write(GPIO_nCS, 1)
        # Set SCLK pin 1/0
        def _clk(self, bit):
            self.pi.write(GPIO_SCLK, bit)
        # Set MOSI pin Output
        def _mosi_output(self):
            self.pi.set_mode(GPIO_MOSI, pigpio.OUTPUT)
            self.pi.write(GPIO_MOSI, 0)  # MOSI = 0
        # CNVST pulse
        def _cnvst(self):
            if(_debug):
                print("\t_cnvst")
            self.pi.write(GPIO_CNVST, 1)  # PIN_CNVST = High
            self.pi.write(GPIO_CNVST, 0)  # PIN_CNVST = Low
        def _rd_miso(self):
            bit =self.pi.read(GPIO_MISO)
            return bit
        # Set MOSI pin Input
        def _mosi_input(self):
            self.pi.set_mode(GPIO_MOSI, pigpio.INPUT)
            self.pi.set_pull_up_down(GPIO_MOSI, pigpio.PUD_DOWN) # pull down    
        
        # Write a WORD(16bits)
        def _wr(self, data):
            self._select()
            if(_debug):
                print("\t_spi_wr: ", hex(data))
            self._mosi_output()
            for i in range(16):
                self._clk(0)
                bit = 1 if((data<<(i) & 0x8000)) else 0
                self.pi.write(GPIO_MOSI, bit)
                self._clk(1)
                
            self._clk(0)
            self.pi.write(GPIO_MOSI, 0)  
            self._deselect()
            
        # Read a byte/word
        # length: 8 or 16
        # return : read data
        def _rd(self, length=8):
            data = 0
            self._mosi_input()
            self._select()
            for i in range(length):
                self._clk(0)
                data = data<<1
                bit = self.pi.read(GPIO_MOSI)
                data += bit
                self._clk(1)
            
            self._clk(0)
            self._deselect()
            if(_debug):
                print("\t_rd: {:02x}".format(data))
            return data
        
        # Reset AD5700
        def _reset57(self):
            self.pi.write(GPIO_nRESET, 0)  # PIN_nRESET = Low
            self.pi.write(GPIO_nRESET, 1)  # PIN_nRESET = High
        # Set RTS AD5700    
        def _rts(self,state=1):
            self.pi.write(GPIO_nRTS, state)  # PIN_nRTS = High:demod,Low:mod
        # Read CD
        def _det_cd(self):
            bit =self.pi.read(GPIO_CD)
            return bit
        
        # destructor
        def __del__(self):
            self.pi.stop()          # Stop handling pin         
### end of spi.py