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
HOST = '10.49.234.234'
PORT = 2055
#HOST = '127.0.0.1'
#PORT = 631
BIN_LONG_TRANCE = 4000
CRLF = '\r\n'
TIMEOUT = 5 # seconds
BUFFSIZE = 8192 # 4096*2 = 8192 bytes = 8kbytes

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
def command_to_licel(sock,command,wait):
  try:
    response=None
    print('Sending:',command)
    sock.send(bytes(command + CRLF,'utf-8'))
    sock.settimeout(TIMEOUT)
    
    if wait!=0:
      time.sleep(wait) # wait TCP adquisition
    
    response = sock.recv(BUFFSIZE).decode()
    print("Received from server:",response)
    print("msg len:",len(response),"type:",type(response))

  except Exception as e:
    raise e
  finally:
    return response

def licel_selectTR(sock,tr):
  command = "SELECT" + " " + str(tr)
  response = command_to_licel(sock,command,0)
  
  if "executed" not in response:
    print("Licel_TCPIP_SelectTR - Error 5083:", command)
    return -5083
  else:
    return 0

def licel_setInputRange(sock,inputrange):
  command = "RANGE"+ " " + inputrange
  response = command_to_licel(sock,command,0)

  if "set to" not in response:
    print("Licel_TCPIP_SetInputRange - Error 5097:", command)
    return -5097
  else:
    return 0

def licel_setThresholdMode(sock,thresholdmode):
  command = "THRESHOLD"+ " " + thresholdmode
  response = command_to_licel(sock,command,0)

  if "set to" not in response:
    print("Licel_TCPIP_SetThresholdMode - Error 5098:", command)
    return -5098
  else:
    return 0

def licel_setDiscriminatorLevel(sock,discriminatorlevel):
  command = "DISC"+ " " + discriminatorlevel
  response = command_to_licel(sock,command,0)

  if "set to" not in response:
    print("Licel_TCPIP_SetDiscriminatorLevel - Error 5096:", command)
    return -5096
  else:
    return 0

def licel_msDelay(delay):
  time.sleep(delay/1000) # delay on seconds

def licel_clearMemory(sock):
  command = "CLEAR"
  response = command_to_licel(sock,command,0)

  if "executed" not in response:
    print("LLicel_TCPIP_ClearMemory - Error 5092:", response)
    return -5092
  else:
    return 0

def licel_startAcquisition(sock):
  command = "START"
  response = command_to_licel(sock,command,0)

  if "executed" not in response:
    print("Licel_TCPIP_SingleShot - Error 5095:", response)
    return -5095
  else:
    return 0

def licel_stopAcquisition(sock):
  command = "STOP"
  response = command_to_licel(sock,command,0)

  if "executed" not in response:
    print("Licel_TCPIP_SingleShot - Error 5095:", response)
    return -5095
  else:
    return 0

def licel_waitForReady(sock,delay):
# start_ms = round(time.time()*1000) # epcoch system time in ms
# while(start_ms + delay > round(time.time()*1000)):
  pass

def licel_parseStatus(sock):
  command = "STAT?"
  response = command_to_licel(sock,command,0)
  memory = 0
  acquisitionstate = False
  recording = False
  shotnumber = 0

  if "Shots" in response:
    shotnumber = int(response.split()[1])
    
    if "Armed" in response:
      acquisitionstate = True
      recording = True

    if "MemB" in response:
      memory = 1

    #TODO class attributes STAT
    return shotnumber,memory,acquisitionstate,recording 

  else:
    return 0,0,False,False

def licel_getStatus(sock):
  command = "STAT?"
  response = command_to_licel(sock,command,0)

  if "Shots" in response:
    return 0
  else:
    print("Licel_TCPIP_GetStatus - Error 5765:", response)
    return -5765

def licel_getDatasets(sock,device,dataset,bins,memory):
  command = "DATA?" + " " + str(device) \
                    + " " + str(bins) \
                    + " " + str(dataset) \
                    + " " + str(memory)
  delay = 2 # seconds
  databuff=b'0'
  try:
    while(len(databuff) < 2*bins):
      print('Sending:',command)
      sock.send(bytes(command + CRLF,'utf-8'))
      sock.settimeout(TIMEOUT)
      time.sleep(delay) # wait TCP adquisition 
    
      databuff = sock.recv(BUFFSIZE)
      print("databuff len:",len(databuff))
      delay += 1

  except Exception as e:
    raise e
  
  dataout = np.frombuffer(databuff,dtype=np.uint16)
  return dataout

# (unsigned short* i_lsw,unsigned short* i_msw,int iNumber, long *lAccumulated, short *iClipping)

def licel_combineAnalogDatasets(i_lsw,i_msw,iNumber):
  MSW_ACUM_MASK=0xFF
  LSW_CLIP_MASK=0x100

  accum = np.left_shift(i_msw & MSW_ACUM_MASK, 16) + i_lsw
  clip = np.right_shift(i_msw & LSW_CLIP_MASK, 8)
 
  return accum.astype(np.float64),clip.astype(np.uint16)

def licel_normalizeData(lAccumulated, iNumber, iCycles):
  
  dNormalized=np.zeros(iNumber,dtype=np.float64)
  
  if iCycles==0:
    dNormalized=np.array(lAccumulated,dtype=np.float64)
  else:
    dNormalized=np.array(lAccumulated,dtype=np.float64)/iCycles
    
  return dNormalized

def licel_scaleAnalogData(dNormalized, iNumber, iRange):

  # 2^12 = 4096 bits max Licel ADC counts 
  
  scale = 0.0
  if iRange == MILLIVOLT500:
    scale=500.0/4096.0
  elif iRange == MILLIVOLT100:
    scale=100.0/4096.0
  elif iRange == MILLIVOLT20:
    scale=20.0/4096.0
  else:
    scale=1.0

  # scaling 
  data_mv = np.array(dNormalized)*scale
  
  return data_mv

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
  # licel_setThresholdMode(sock,THRESHOLD_LOW)
  # licel_setDiscriminatorLevel(sock,DISCRIMINATOR_LEVEL)
  
  ## select another TR and confgure it here
  
  # START THE ACQUISITION

  ## wait for one sec
  ## this would be the loop start for continous acquisitions
  licel_clearMemory(sock)
  licel_startAcquisition(sock)

  licel_msDelay(2000) # wait 1000ms
  licel_stopAcquisition(sock) # stop the TR
  # licel_waitForReady(sock,100) # wait till it returns to the idle state

  ## get the shotnumber
  ## iCycles must be long int
  if licel_getStatus(sock) == 0:
    iCycles,iMemory,iAcq_State,iRecording = licel_parseStatus(sock) 
    if (iCycles > 1):
      iCycles -= 2;

  # READ FROM THE TR

  ## read the analog LSW and MSW
  ## buffer preparation
  iNumber = BIN_LONG_TRANCE ## read a 2000 bin long trace
    
  data_lsw = np.zeros(2*(iNumber+1),np.uint16)
  data_msw = np.zeros(2*(iNumber+1),np.uint16)

  data_lsw = licel_getDatasets(sock,tr,"LSW",iNumber+1,"A")
  data_msw = licel_getDatasets(sock,tr,"MSW",iNumber+1,"A")
  
  ## combine them and transfer it into mV
  data_accu = np.zeros(iNumber,np.uint64) # combined binary data
  data_clip = np.zeros(iNumber,np.uint16) # clip information
  data_phys = np.zeros(iNumber,np.float64) # normalized to the shotnumber (double)
  data_mv = np.zeros(iNumber,np.float64) # and mV data (double)

  data_accu,data_clip = licel_combineAnalogDatasets(data_lsw, data_msw, iNumber+1)
  
  # Normalizes the accumulated Data with respect to the number of cycles
  data_phys = licel_normalizeData(data_accu, iNumber, iCycles)
  
  # data to mV
  data_mv = licel_scaleAnalogData(data_phys, iNumber, MILLIVOLT500) 
  
  # DUMP THE DATA INTO A FILE
  with open('analog.txt', 'w') as file: # or analog.dat 'wb'
    np.savetxt(file,data_mv,delimiter=',')


  # Plot
  t = np.arange(0, len(data_mv), 1)
  fig, ax = plt.subplots()
  ax.plot(t, data_mv)
  ax.set(xlabel='bins', ylabel='voltage (mV)',title='SMN LICEL')
  ax.grid()
  fig.savefig("test.png")
  plt.show()
