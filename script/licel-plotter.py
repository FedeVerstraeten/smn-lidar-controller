#!/usr/bin/env python3
import sys
import socket
import time
import numpy as np
import matplotlib.pyplot as plt

HOST = '10.49.234.234'
PORT = 2055

def command_to_licel(licelcommand):
  data=None
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(bytes(licelcommand+'\r\n','utf-8'))
    time.sleep(2) # wait TCP adquisition
    data = s.recv(8192) # 8192 = 4096 * 2
    print("Len:",len(data),"type:",type(data))
  return data

if __name__ == '__main__':
    # Select TR
    command_select='SELECT 0'
    rsp=repr(command_to_licel(command_select))
    print('Received',rsp) 
    
    # Clear memory
    command_clear='MCLEAR'
    rsp=repr(command_to_licel(command_clear))
    print('Received',rsp) 
    
    # Start TR 
    command_start='MSTART'
    rsp=repr(command_to_licel(command_start))
    print('Received',rsp) 
    
    time.sleep(5)

    # Stop TR 
    command_stop='MSTOP'
    rsp=repr(command_to_licel(command_stop))
    print('Received',rsp) 
 
    # Get data 
    command_data='DATA? 0 4001 LSW A'
    rsp=command_to_licel(command_data)
    #print('Received',rsp) 
   # with open('outputlicel', 'w') as f:
   #   f.write(rsp)
    data_output=rsp
    
    # Plot
    t = np.arange(0, len(data_output), 1)
    data_arr=[]
    for data_byte in data_output:
      data_arr.append(int(data_byte))
    fig, ax = plt.subplots()
    ax.plot(t, data_arr)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',title='SMN LICEL')
    ax.grid()
    fig.savefig("test.png")
    plt.show()
