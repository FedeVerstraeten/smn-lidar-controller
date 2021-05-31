#!/usr/bin/env python3
import sys
import socket

HOST = '10.49.234.234'
PORT = 2055

def command_to_licel(licelcommand):
  data=None
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print('Command to execute:',licelcommand)
    s.sendall(bytes(licelcommand+'\r\n','utf-8'))
    data = s.recv(1024)
  return data

if __name__ == '__main__':
  if len(sys.argv) > 1:
    rsp=repr(command_to_licel(str(sys.argv[1])))
    print('Received',rsp) 
  else:
    print('ERROR arguments needed')

