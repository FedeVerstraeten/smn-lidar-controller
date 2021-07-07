#!/usr/bin/env python3

"""
This program will:
- open a connection
- configure a TR
- start the acquisition, wait for one sec
- read from the TR the analog and photon counting data back
- dump the data into a file
"""

# Libraries

import sys
import socket
import time
import numpy as np
import matplotlib.pyplot as plt

# Global parameters
# HOST = '10.49.234.234'
# PORT = 2055
HOST = '127.0.0.1'
PORT = 631
BIN_LONG_TRANCE=2000

## Input Ranges
MILLIVOLT500 = 0
MILLIVOLT100 = 1
MILLIVOLT20  = 2

## Threshold Modes
THRESHOLD_LOW  = 0
THRESHOLD_HIGH = 1

## Datasets
PHOTON = 0
LSW    = 1
MSW    = 2

## Memory
MEM_A = 0
MEM_B = 1

# Functions

def licel_selectTR(sock,tr):
  pass

def licel_msDelay(delay):
  pass

def licel_startAcquisition(sock):
  pass

def licel_stopAcquisition(sock):
  pass

def licel_waitForReady(sock,delay):
  pass

def  licel_getStatus(sock):
  pass

def licel_getDatasets(sock,tr,dataset,bin,mem):
  pass

def licel_combineAnalogDatasets():
  pass

def licel_normalizeData():
  pass

def licel_scaleAnalogData():
  pass

# Main

if __name__ == '__main__':

  # OPEN A CONNECTION
  
  sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  server_address = (HOST,PORT)
  
  try:
    print('Connecting to: ', server_address)
    sock.connect(server_address)
    print('Connected to server')
  except Exception as e:
    raise ValueError("Connection to server failed")
 
  # CONFIGURE A TR

  tr = 0 # using the first Transient Recorder
  licel_selectTR(sock,tr)
  # licel_setInputRange(sock,MILLIVOLT500)
  # licel_selectTR(sock,THRESHOLD_LOW)
  # licel_setDiscriminatorLevel(sock,DISCRIMINATOR_LEVEL)
  
  ## select another TR and confgure it here
  
  # START THE ACQUISITION

  ## wait for one sec
  ## this would be the loop start for continous acquisitions
  
  licel_startAcquisition(sock)

  licel_msDelay(1000) # wait 1000ms
  licel_stopAcquisition(sock) # stop the TR
  licel_waitForReady(sock,100) # wait till it returns to the idle state

  ## get the shotnumber
  ## iCycles must be long int
  iCycles,iMemory,iAcq_State,iRecording = licel_getStatus(sock) 
  if (iCycles > 1):
    iCycles -= 2;

  # READ FROM THE TR

  ## read the analog LSW and MSW
  ## buffer preparation
  iNumber = BIN_LONG_TRANCE ## read a 2000 bin long trace
    
  data_LSW = np.zeros(2*(iNumber+1),np.uint32)
  data_MSW = np.zeros(2*(iNumber+1),np.uint32)

  data_LSW = licel_getDatasets(sock,tr,LSW,iNumber+1,MEM_A)
  data_MSW = licel_getDatasets(sock,tr,MSW,iNumber+1,MEM_B)
  
  ## combine them and transfer it into mV
  data_accu = np.zeros(iNumber,np.uint64) # combined binary data
  data_clip = np.zeros(iNumber,np.uint32) # clip information
  data_phys = np.zeros(iNumber,np.float64) # normalized to the shotnumber (double)
  data_mV = np.zeros(iNumber,np.float64) # and mV data (double)

  data_accu,data_clip = licel_combineAnalogDatasets(data_LSW, data_MSW, iNumber+1)
  
  # Normalizes the accumulated Data with respect to the number of cycles
  data_phys = licel_normalizeData(data_accu, iNumber, iCycles)
  
  # data to mV
  data_mV = licel_scaleAnalogData(data_phys, iNumber, MILLIVOLT500) 
  
  # DUMP THE DATA INTO A FILE
  with open('analog.txt', 'w') as file: # or analog.dat 'wb'
    # for (i=0; i< iNumber; i++) {
    #   fprintf(fp,"%g\n", data_mV[i]);
    # }
    file.write(rsp)