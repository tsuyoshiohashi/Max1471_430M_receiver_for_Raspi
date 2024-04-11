#!/usr/bin/env python3
#
# rxafsk.py
# driver fot raspi max1471+ad5700+max1117 430M receiver hat(my own work, see hat directory)
# 
# This implementation is for personal experiments.
# Copyright (c) 2024 Tsuyoshi Ohashi
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php
#
import pigpio
import time
import readline
import os

from rxafskconst import *
from spi import Spi
from regs import *

__version__ = "2024.3.21"

# debug flag
debug = False   #True

class RxAfsk:
        
    def __init__(self):
        self.reg0 = Reg0()
        self.reg1 = Reg1()
        self.reg2 = Reg2()
        self.reg3 = Reg3()
        self.spi = Spi()          
    #
    def reset_master(self):
        cmd = CMD_RESET
        adrs = 0x0
        data = 0x0
        to_send = cmd<<12 | adrs<<8 | data
        self.spi._wr( to_send)
    
    # get register_9 ( Status Register)
    def read_reg9(self):
        cmd = CMD_READ
        adrs = 0x9
        data = 0x0
        to_send = cmd<<12 | adrs<<8 | data
        self.spi._wr(to_send)
        rd_data = self.spi._rd()
        lockdet = (rd_data>>7) & 0b1
        agcst = (rd_data>>6) & 0b1
        clkalive = (rd_data>>5) & 0b1
        pol_cal_done = (rd_data>>1) & 0b1
        fsk_cal_done = rd_data & 0b1

        return lockdet, agcst, clkalive, pol_cal_done, fsk_cal_done
    
    def get_ld(self):
        lockdet,_,_,_,_= self.read_reg9()
        return lockdet
        
    def setup(self):
        if(debug):
            print("setup")
            
        # Send Master Reset command
        self.reset_master()        
        
        # write registers max1471
        self.reg0.write()
        self.reg3.write()
        self.reg1.write()    
        self.reg2.write() 
        # setup ad5700
        self.spi._reset57()
        self.spi._rts(1)
        
    # Read voltage(ch0=RSSI, ch1=AFSK) 
    # return : voltage
    def get_adc_reading(self, ch=0):
        if(debug):
            print("get_adc_reading")
        # ch1 only
        if(ch==1):
            self.spi._cnvst()
        # ch0 and ch1
        self.spi._cnvst()
        data = 0
        self.spi._clk(0)
        for _ in range(8):
            self.spi._clk(1)
            data = data<<1
            bit = self.spi._rd_miso()
            data += bit
            self.spi._clk(0)
        
        return data
   
    #
    def __del__(self):
        del self.reg0
        del self.reg1
        del self.reg2
        del self.reg3
        del self.spi

### TEST ###
# help message 
def show_help():
    print("commands: ")
    print("reset: reset and initialize MAX1471 and AD5700")
    print("rssi/r: get and show rssi")
    print("cal/fskcal: Calibrate FSK demod")
    print("read/rd n : Read register n(0-3)")
    print("read/rd cd : Read CD signal")
    print("write/wr n m : Read register n(0-3) data m(hex)")
    print("help : Show this help")

###
if __name__ == '__main__':
    print("rxafsk.py  ver.", __version__ )
    
    rxafsk = RxAfsk()
    # setup, reset and initialize 
    rxafsk.setup()
    
    # read reg9
    lockdet, agcst, clkalive, pol_cal_done, fsk_cal_done = rxafsk.read_reg9()
    print("lockdet:", lockdet)
    print("agcst:", agcst)
    print("clkalive:", clkalive)
    print("pol_cal_done:", pol_cal_done)
    print("fsk_cal_done:", fsk_cal_done)
    
    ###
    HISTORY_FILE = os.path.expanduser('~/.rxafsk_history')
    if os.path.exists(HISTORY_FILE):
        readline.read_history_file(HISTORY_FILE)
    ### Let's go!
    while(1):
        lockdet, agcst, clkalive, pol_cal_done, fsk_cal_done = rxafsk.read_reg9()
        p_start = "\033[32m" if (lockdet) else "\033[31m"   # Lock:Green/ Unlock:Red 
        p_end = "\033[0m"
        p1 = ">"
        p2 = "H" if(agcst==1) else ("L")
        #p2,p3,p4,p5 = str(agcst), str(clkalive), str(pol_cal_done), str(fsk_cal_done)
        cmd_line = input( p_start + p2 + p1 + p_end)
        readline.write_history_file(HISTORY_FILE)
        cmd = cmd_line.split()
        if( len(cmd)==0):
            pass
        elif(cmd[0]=="reset"):
            rxafsk.setup()
            
        elif(cmd[0]=="rssi" or cmd[0]=="r"):
            rssi_lvl = rxafsk.get_adc_reading(ch=0)
            #print("rssi: ", rssi_lvl)
            rssi_vol = 2.048 *rssi_lvl / 256
            print(f"rssi : { rssi_vol:.3f}　V")
            #_,agcst,_,_,_ = rxafsk.read_reg9()
            #print("agcst:", agcst)
            
        elif(cmd[0]=="cal" or cmd[0]=="fskcal"):
            rxafsk.reg2.fsk_cal_en = 1
            rxafsk.reg2.write()
            _, _, _, _, fsk_cal_done = rxafsk.read_reg9()
            print("fsk_cal_done:", fsk_cal_done)
            
        # Read Register 0-3,9 and CD   
        elif(cmd[0]=="read" or cmd[0]=="rd"):
            try:
                if(cmd[1]=="0"):
                    rd_data = rxafsk.reg0.read()
                    print("Reg",cmd[1],"= {:08b}".format(rd_data))
                elif(cmd[1]=="1"):
                    rd_data = rxafsk.reg1.read()
                    print("Reg",cmd[1],"= {:08b}".format(rd_data))
                elif(cmd[1]=="2"):
                    rd_data = rxafsk.reg2.read()
                    print("Reg",cmd[1],"= {:08b}".format(rd_data))
                elif(cmd[1]=="3"):
                    rd_data = rxafsk.reg3.read()
                    print("Reg",cmd[1],"= {:08b}".format(rd_data))
                elif(cmd[1]=="9"):
                    rd_data = rxafsk.read_reg9()
                    print("Reg",cmd[1],"= ", rd_data)
                elif(cmd[1]=="cd"):
                    bit_cd = rxafsk.spi._det_cd()
                    print("CD: ", bit_cd)
                else:
                    print("Specify correct register no")
            except:
                print("Specify register no")    
                
        # Write Register 0-3   
        elif(cmd[0]=="write" or cmd[0]=="wr"):
            try:
                wr_data = int(cmd[2],16)
                if(cmd[1]=="0"):
                    rxafsk.reg0.power_config = wr_data
                    rxafsk.reg0.write()
                elif(cmd[1]=="1"):
                    rxafsk.reg1.config = wr_data
                    print(hex(wr_data))
                    rxafsk.reg1.write()
                elif(cmd[1]=="2"):
                    rxafsk.reg2.control = wr_data
                    rxafsk.reg2.write()
                elif(cmd[1]=="3"):
                    rxafsk.reg3.xtal = wr_data
                    rxafsk.reg3.write()
            except:
                print("Invalid command")   
                
        ## quit/exit
        elif(cmd[0]=="quit" or cmd[0]=="exit" or cmd[0]=="q" or cmd[0]=="e"):
            print("Bye!")
            exit()
        elif(cmd[0]=="help" or cmd[0]=="h"):
             show_help()        
        # unknown command
        else:
            print("Sorry,not in command list.")
            show_help()    
    # 
    del rxafsk
### end of rxafsk.py