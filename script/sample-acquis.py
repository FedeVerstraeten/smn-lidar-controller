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
BIN_LONG_TRANCE = 2000
CRLF = '\r\n'
TIMEOUT = 1 # seconds

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
def command_to_licel(sock,command):
  try:
    resp=None
    print('Sending:',command)
    sock.settimeout(TIMEOUT)
    sock.sendall(bytes(command + CRLF,'utf-8'))
    #time.sleep(2) # wait TCP adquisition
    resp = sock.recv(8192).decode() # 8192 = 4096 * 2
    print("Received from server:",resp)
    print("msg len:",len(resp),"type:",type(resp))

  except Exception as e:
    raise e
  finally:
    return resp

def licel_selectTR(sock,tr):

  command = "SELECT " + str(tr)
  resp = command_to_licel(sock,command)
  
  if "executed" not in resp:
    print("Licel_TCPIP_SelectTR - Error 5083:", command)
    return -5083
  else:
    return resp

def licel_setInputRange(sock,MILLIVOLT500):
  # char command[1000];
  # sprintf(command,"RANGE  %d\r\n", inputRange);
  # writeCommand(s, command);
  # int rv = readResponse(s, command, 200, 1000);
  # if (rv < 0)
  #   return rv;
  #  if (!strstr(command,"set to")) {
  #    printf("\r\nLicel_TCPIP_SetInputRange - Error 5097 :%s", command);
  #    return -5097;
  # }
  # return 0;
  pass

def licel_setThresholdMode(sock,THRESHOLD_LOW):
  # char command[1000];
  # sprintf(command,"THRESHOLD %d\r\n", thresholdMode);
  # writeCommand(s, command);
  # int rv = readResponse(s, command, 200, 1000);
  # if (rv < 0)
  #   return rv;
  #  if (!strstr(command,"THRESHOLD")) {
  #    printf("\r\nLicel_TCPIP_SetThresholdMode - Error 5098 :%s", command);
  #    return -5098;
  # }
  # return 0; 
  pass

def licel_setDiscriminatorLevel(sock,DISCRIMINATOR_LEVEL):
  # char command[1000];
  # sprintf(command,"DISC %d\r\n", discriminatorLevel);
  # writeCommand(s, command);
  # int rv = readResponse(s, command, 200, 1000);
  # if (rv < 0)
  #   return rv;
  #  if (!strstr(command,"set to")) {
  #    printf("\r\nLicel_TCPIP_SetDiscriminatorLevel - Error 5096 :%s", command);
  #    return -5096;
  # }
  # return 0; 
  pass


def licel_msDelay(delay):
#   #ifdef _CVI_
#   Delay((double) Milliseconds/1000.0);
# #else
#   Sleep(Milliseconds);
# #end
  pass

def licel_startAcquisition(sock):
  # writeCommand(s, "START \r\n");
  # char response[1000];
  # int rv = readResponse(s, response, 200, 1000);
  # if (rv < 0)
  #   return rv;
  # if (strcmp(response,"START executed")) {
  #   printf("\r\nLicel_TCPIP_SingleShot - Error 5095 :%s", response);
  #   return -5095;
  # }
  # return 0;
  pass

def licel_stopAcquisition(sock):
  # writeCommand(s, "START \r\n");
  # char response[1000];
  # int rv = readResponse(s, response, 200, 1000);
  # if (rv < 0)
  #   return rv;
  # if (strcmp(response,"START executed")) {
  #   printf("\r\nLicel_TCPIP_SingleShot - Error 5095 :%s", response);
  #   return -5095;
  # }
  # return 0;
  pass

def licel_waitForReady(sock,delay):
# #ifdef WIN32
#   DWORD start = GetTickCount();
# #else
#   struct timeb t1, t2;
#   double duration;
#   ftime(&t1);
# #endif
#   do {
#     long int shotNumber;
#     int memory;
#     int acquisitionState, recording;
#     int rv = Licel_TCPIP_GetStatus(s, &shotNumber, &memory, &acquisitionState, &recording);
#     if (rv < 0)
#       return rv;
#     if (!acquisitionState)
#       return rv;
# #ifdef WIN32
#   } while (start + Delay > GetTickCount());
# #else
#   ftime(&t1);
#   duration = (1000.0*(t2.time-t1.time)+t2.millitm-t1.millitm);  
# } while (duration < Delay); // + (start.millitm - now.millitm));  
# #endif
#   return -5700;
  pass

def  licel_getStatus(sock):
  # writeCommand(s, "STAT?\r\n");
  # char response[1000];
  # int rv = readResponse(s, response, 200, 1000);
  # if (rv < 0)
  #   return rv;
  # if (strstr(response,"Shots")) {
  #   *memory = 0;
  #   *acquisitionState = false;
  #   * recording = false;
  #   sscanf(response, "Shots %ld", shotNumber);
  #   if (strstr(response,"Armed"))
  #     *acquisitionState = true;
  #   if (strstr(response,"Armed"))
  #     *recording = true;
  #   if (strstr(response,"MemB"))
  #     *memory = 1;
  #   return 0;
  # }
  # else {
  #   printf("\r\nLicel_TCPIP_GetStatus - Error 5765 :%s", response);
  #   return -5765;
  # }
  pass

def licel_getDatasets(sock,tr,dataset,bin,mem):
  # char command[1000];
  # sprintf(command,"DATA? %d %d", device, numberToRead);
  # switch (dataSet) {
  # case 0: 
  #   strcat(command, " PHO");
  #   break;
  # case 1: 
  #   strcat(command, " LSW");
  #   break;
  # case 2:
  #   strcat(command, " MSW");
  #   break;
  # }
  # if (!Memory)
  #   strcat (command, " A");
  # else
  #   strcat (command, " B");
  # strcat(command,"\r\n");
  # int rv = writeCommand(s, command);
  # if (rv < 0)
  #   return rv;
  #  return Licel_TCPIP_ReadData(s, numberToRead, data);
  pass

def licel_combineAnalogDatasets():
  # int i;
  # for(i=1;i<iNumber;i++)
  # {
  #   lAccumulated[i-1]=(long) i_lsw[i] + (((long) i_msw[i]&0xFF)<<16);
  #   iClipping[i-1]=(short) ((i_msw[i]&0x100)>>8);
  # }
  pass

def licel_normalizeData():
  # int i;
  # if(iCycles==0)
  #   iCycles=1;
  # for(i=0;i<iNumber;i++)
  # {
  #   dNormalized[i]=lAccumulated[i]/(double) iCycles;
  # }
  pass

def licel_scaleAnalogData():
  # int i;
  # double dScale;
  # switch(iRange)
  # {
  #   case MILLIVOLT500:
  #              dScale=500.0/4096.0;
  #           break;
  #   case MILLIVOLT100:
  #              dScale=100.0/4096.0;
  #           break;
  #   case MILLIVOLT20:  dScale=20.0/4096.0;
  #           break;
  #   default:      dScale=1.0;
  #           break;
  # }
  # for(i=0;i<iNumber;i++)
  # {
  #   dmVData[i]=dScale*dNormalized[i];
  # }
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
  # licel_setThresholdMode(sock,THRESHOLD_LOW)
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