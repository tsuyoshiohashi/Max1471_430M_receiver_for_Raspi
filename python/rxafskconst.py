#
# rxafskconst.py
# parameters for regs.py, spi.py and rxafsk.py 

# This implementation is for personal experiments.
# Copyright (c) 2024 Tsuyoshi Ohashi
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

# GPIO pin config
# device_name - BCM# - raspi_IO_pin#
# SoftSPI (NOT BCM system SPI)
GPIO_nCS = 8   # GPIO8 = pin24
GPIO_MOSI = 10    # GPIO10 = pin19  # max1471 Bi-directional

GPIO_MISO = 9    # GPIO9 = pin21    # max1117(ADC)
GPIO_SCLK = 11   # GPIO11 = pin23

GPIO_nRTS = 13  # GPIO13 = pin33
GPIO_nRESET = 26 # GPIO26 = pin37
GPIO_CD = 19 # GPIO19 = pin35
TXD = 8 #  
RXD = 10 # 

#max1117
# down edge starts convert
# 1 edge for CH0, 2 edgs for CH1
GPIO_CNVST = 7 # GPIO7 = pin26
 
#GPIO1 = 6   # GPIO6 = pin31
#GPIO2 = 27  # GPIO27 = pin13
#GPIO3 = 17  # GPIO17 = pin11
#GPIOSDN = 4 # GPIO4 = pin7
#GPIOnIRQ = 5   # GPIO05 = pin29

# Config GPIO
#GPIO_TX_DATA = GPIO0 
#GPIO_CTS = GPIO1
#GPIO_SHDN = GPIOSDN

# Commands for max1471
CMD_NOP = 0x0
CMD_WRITE = 0x1
CMD_READ = 0x2
CMD_RESET = 0x3

# Registers in max1471
REG_PWR_CFG = 0x0
REG_CONFIG = 0x1
REG_CONTROL = 0x2
REG_OSC_FREQ = 0x3
REG_STATUS = 0x9
REG_AGC_DWELL = 0xA

# XTAL
FREQ_XTAL = 0x84  # 13.2256MHz/100kHz=132=0x84 

###