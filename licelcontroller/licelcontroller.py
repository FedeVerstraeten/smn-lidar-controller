#!/usr/bin/env python3

"""
This class will:
- open a connection
- configure a TR
- start the acquisition, wait for one sec
- read from the TR the analog and photon counting data back
- dump the data into a file
"""

# Sys libraries
import os
import sys
# __dir__ = os.path.dirname(__file__)
# path = os.path.join(__dir__,'packages')
# sys.path.insert(0,path)

# Libraries
import time
import socket
import numpy as np

class licelcontroller:

  # ATTRIBUTES:

  def __init__(self):

    # TCP/IP socket
    self.host = '10.49.234.234'
    self.port = 2055
    self.sock = None
    self.buffersize = 8192 # 4096*2 = 8192 bytes = 8kbytes
    
    # Licel parameters
    self.transient_recorder = 0 
    self.bin_long_trace = 4000
    self.shots_delay = 10000 # wait 10s = 300shots/30Hz
    self.timeout = 5 # seconds

    self.memory = 0
    self.acquisitionstate = False
    self.recording = False
    self.shotnumber = 0

  # METHODS:
  
  def openConnection(self,host,port):
    self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_address = (host,port)
  
    try:
      print('Connecting to: ', server_address)
      self.sock.connect(server_address)
      print('Connected to server')
    except Exception as e:
      raise ValueError("Connection to server failed")

  def runCommand(self,command,wait):
    response=None
    try:
      print('Sending:',command)
      self.sock.send(bytes(command + '\r\n','utf-8'))
      self.sock.settimeout(self.timeout)
      
      if wait!=0:
        time.sleep(wait) # wait TCP adquisition
      
      response = self.sock.recv(self.buffersize).decode()
      print(f"Received from server: {response} msg len: {len(response)}")

    except Exception as e:
      raise e
    finally:
      return response

  def selectTR(self,transientrecorder):
    command = "SELECT" + " " + str(transientrecorder)
    waitsecs = 0
    response = self.runCommand(command,waitsecs)
  
    if "executed" not in response:
      print("Licel_TCPIP_SelectTR - Error 5083:", command)
      return -5083
    else:
      return 0

  def setInputRange(self,inputrange):
    command = "RANGE"+ " " + str(inputrange)
    waitsecs = 0
    response = self.runCommand(command,waitsecs)

    if "set to" not in response:
      print("Licel_TCPIP_SetInputRange - Error 5097:", command)
      return -5097
    else:
      return 0

  def setThresholdMode(self,thresholdmode):
    command = "THRESHOLD"+ " " + thresholdmode
    waitsecs = 0
    response = self.runCommand(command,waitsecs)

    if "set to" not in response:
      print("Licel_TCPIP_SetThresholdMode - Error 5098:", command)
      return -5098
    else:
      return 0

  def setDiscriminatorLevel(self,discriminatorlevel):
    command = "DISC"+ " " + discriminatorlevel
    waitsecs = 0
    response = self.runCommand(command,waitsecs)

    if "set to" not in response:
      print("Licel_TCPIP_SetDiscriminatorLevel - Error 5096:", command)
      return -5096
    else:
      return 0


  def clearMemory(self):
    command = "CLEAR"
    waitsecs = 0
    response = self.runCommand(command,waitsecs)

    if "executed" not in response:
      print("Licel_TCPIP_ClearMemory - Error 5092:", response)
      return -5092
    else:
      return 0

  def startAcquisition(self):
    command = "START"
    waitsecs = 0
    response = self.runCommand(command,waitsecs)

    if "executed" not in response:
      print("Licel_TCPIP_SingleShot - Error 5095:", response)
      return -5095
    else:
      return 0

  def stopAcquisition(self):
    command = "STOP"
    waitsecs = 0
    response = self.runCommand(command,waitsecs)

    if "executed" not in response:
      print("Licel_TCPIP_SingleShot - Error 5095:", response)
      return -5095
    else:
      return 0

  def getStatus(sock):
  # def parseStatus(sock):
    command = "STAT?"
    waitsecs = 0
    response = self.runCommand(command,waitsecs)

    if "Shots" in response:
      self.shotnumber = int(response.split()[1])
      
      if "Armed" in response:
        self.acquisitionstate = True
        self.recording = True

      if "MemB" in response:
        self.memory = 1

      #TODO class attributes STAT
      # return shotnumber,memory,acquisitionstate,recording 
      return 0

    else:
      self.memory = 0
      self.acquisitionstate = False
      self.recording = False
      self.shotnumber = 0

      print("Licel_TCPIP_GetStatus - Error 5765:", response)
      return -5765

  # def licel_getDatasets(sock,device,dataset,bins,memory):
  #   command = "DATA?" + " " + str(device) \
  #                     + " " + str(bins) \
  #                     + " " + str(dataset) \
  #                     + " " + str(memory)
  #   delay = 2 # seconds
  #   databuff=b'0'
  #   try:
  #     while(len(databuff) < 2*bins):
  #       print('Sending:',command)
  #       sock.send(bytes(command + CRLF,'utf-8'))
  #       sock.settimeout(TIMEOUT)
  #       time.sleep(delay) # wait TCP adquisition 
      
  #       databuff = sock.recv(BUFFSIZE)
  #       print("databuff len:",len(databuff))
  #       delay += 1

  #   except Exception as e:
  #     raise e
    
  #   dataout = np.frombuffer(databuff,dtype=np.uint16)
  #   return dataout

  # # (unsigned short* i_lsw,unsigned short* i_msw,int iNumber, long *lAccumulated, short *iClipping)

  # def licel_combineAnalogDatasets(i_lsw,i_msw,iNumber):
  #   MSW_ACUM_MASK=0x00FF
  #   LSW_CLIP_MASK=0x100

  #   accum=np.zeros(len(i_msw)-1,np.uint32)
  #   msw_aux=np.array(i_msw,dtype=np.uint32)
  #   lsw_aux=np.array(i_lsw,dtype=np.uint32)

  #   for i in range(1,len(i_msw)):
  #     accum[i-1] = np.left_shift(msw_aux[i] & MSW_ACUM_MASK, 16) + lsw_aux[i]
    
  #   #accum = (msw_aux[1:] & MSW_ACUM_MASK) << 16 + lsw_aux[1:]

  #   clip = np.right_shift(i_msw[1:] & LSW_CLIP_MASK, 8)
   
  #   return accum.astype(np.float64),clip.astype(np.uint16)

  # def licel_normalizeData(lAccumulated, iNumber, iCycles):
    
  #   dNormalized=np.zeros(iNumber,dtype=np.float64)
    
  #   if iCycles==0:
  #     dNormalized=np.array(lAccumulated,dtype=np.float64)
  #   else:
  #     dNormalized=np.array(lAccumulated,dtype=np.float64)/iCycles
      
  #   return dNormalized

  # def licel_scaleAnalogData(dNormalized, iNumber, iRange):

  #   # 2^12 = 4096 bits max Licel ADC counts
    
  #   scale = 0.0

  #   if iRange == MILLIVOLT500:
  #     scale=500.0/4096.0
  #   elif iRange == MILLIVOLT100:
  #     scale=100.0/4096.0
  #   elif iRange == MILLIVOLT20:
  #     scale=20.0/4096.0
  #   else:
  #     scale=1.0

  #   # scaling 
  #   data_mv = np.array(dNormalized)*scale
    
  #   return data_mv

  def msDelay(delay):
    time.sleep(delay/1000) # delay on miliseconds

  # def licel_waitForReady(sock,delay):
  # # start_ms = round(time.time()*1000) # epcoch system time in ms
  # # while(start_ms + delay > round(time.time()*1000)):
  #   pass