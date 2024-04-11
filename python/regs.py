
#
# regs.py
# registers in max1471 for rxafsk.py
# 
# This implementation is for personal experiments.
# Copyright (c) 2024 Tsuyoshi Ohashi
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php
#
from rxafskconst import *
from spi import Spi

class Reg0:
    def __init__(self):
        self.spi = Spi()
        self.lna_en=1
        self.agc_en=1   # 1=en,0=dis
        self.mixer_en=1
        self.fskbb_en=1
        self.fskpd_en=0 # connected to GND
        self.askbb_en=1
        self.askpd_en=1 # RSSI
        self.sleep=0
        self.power_config = self.lna_en<<7 | self.agc_en<<6 | self.mixer_en<<5 | self.fskbb_en<<4 | self.fskpd_en<<3 | self.askbb_en<<2 | self.askpd_en<<1 | self.sleep
       
    def write(self):
        #power_config = self.lna_en<<7 | self.agc_en<<6 | self.mixer_en<<5 | self.fskbb_en<<4 | self.fskpd_en<<3 | self.askbb_en<<2 | self.askpd_en<<1 | self.sleep
        cmd = CMD_WRITE
        adrs = 0x0
        to_send = cmd<<12 | adrs<<8 | self.power_config
        self.spi._wr(to_send)
    
    def read(self):
        to_send = CMD_READ<<12 | 0<<8 | 0x0
        self.spi._wr(to_send)
        rd_data = self.spi._rd()
        return rd_data
        
    def __del__(self):
        del self.spi
    
class Reg1:
    def __init__(self):
        self.spi = Spi()
        self.gainset=0      # 1=High, 0=Low
        self.fskcallsb=1
        self.dout_fsk=0
        self.dout_ask=0
        self.toff_ps1=0
        self.toff_ps0=0
        self.drx_mode=0
        self.config = self.gainset<<6 | self.fskcallsb<<5 | self.dout_fsk<<4 | self.dout_ask<<3 | self.toff_ps1<<2 | self.toff_ps0<<1 | self.drx_mode
      
    def write(self):
        #config = self.gainset<<6 | self.fskcallsb<<5 | self.dout_fsk<<4 | self.dout_ask<<3 | self.toff_ps1<<2 | self.toff_ps0<<1 | self.drx_mode
        cmd = CMD_WRITE
        adrs = 0x1
        to_send = cmd<<12 | adrs<<8 | self.config
        self.spi._wr(to_send)
        
    def read(self):
        to_send = CMD_READ<<12 | 1<<8 | 0x0
        self.spi._wr(to_send)
        rd_data = self.spi._rd()
        return rd_data
    
    def __del__(self):
        del self.spi

class Reg2:
    def __init__(self):
        self.spi = Spi()
        self.agclock=0  # 0
        self.fsktrk_en=0    # 0
        self.asktrk_en=0
        self.pol_cal_en=0
        self.fsk_cal_en=1
        #self.control = self.agclock<<6 | self.fsktrk_en<<3 | self.asktrk_en<<2 | self.pol_cal_en<<1 | self.fsk_cal_en
       
    def write(self):
        self.control = self.agclock<<6 | self.fsktrk_en<<3 | self.asktrk_en<<2 | self.pol_cal_en<<1 | self.fsk_cal_en
        cmd = CMD_WRITE
        adrs = 0x2
        to_send = cmd<<12 | adrs<<8 | self.control
        self.spi._wr(to_send)
    
    def read(self):
        to_send = CMD_READ<<12 | 2<<8 | 0x0
        self.spi._wr(to_send)
        rd_data = self.spi._rd()
        return rd_data
        
    def __del__(self):
        del self.spi
    
class Reg3:
    def __init__(self):
        self.spi = Spi()
        self.xtal = FREQ_XTAL
        
    def write(self):
        cmd = CMD_WRITE
        adrs = 0x3
        data = self.xtal
        to_send = cmd<<12 | adrs<<8 | data
        self.spi._wr(to_send)
        
    def read(self):
        to_send = CMD_READ<<12 | 3<<8 | 0x0
        self.spi._wr(to_send)
        rd_data = self.spi._rd()
        return rd_data
        
    def __del__(self):
        del self.spi

### end of regs.py