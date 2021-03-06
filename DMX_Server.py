from __future__ import print_function
from ola.ClientWrapper import ClientWrapper
import array
import sys

__author__ = 'brian.mcmillan@steeplesquare.co.uk'

from SocketServer import BaseRequestHandler, TCPServer

wrapper = None


def DmxSent(status):
  if status.Succeeded():
    print('Success!')
  else:
    print('Error: %s' % status.message, file=sys.stderr)

  global wrapper
  if wrapper:
    wrapper.Stop()



DMXData = array.array('B')

class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:
            RecvMsg = self.request.recv(512)
            for i in range(10):
                print ('RECV: ', RecvMsg[i],':')
            break
            if not RecvMsg:
              break

        for i in range(512):
            DMXData.insert(i, ord(RecvMsg[i]))
        
        global wrapper
        wrapper = ClientWrapper()
        client = wrapper.Client()
  # send 1 dmx frame
        Universe = 1
        client.SendDmx(Universe, DMXData, DmxSent)
        wrapper.Run()

        
        self.request.send(b'ACK')

if __name__ == '__main__':
    serv =  TCPServer(('', 20000), EchoHandler)
    print('Echo server running on port 20000')
    serv.serve_forever()
