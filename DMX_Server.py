from __future__ import print_function
from ola.ClientWrapper import ClientWrapper
import array
import sys

__author__ = 'nomis52@gmail.com (Simon Newton)'

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

#class EchoHandler(BaseRequestHandler):
#    def handle(self):
#        print('Got connection from', self.client_address)
#        while True:
#            DMXData = self.request.recv(512)
#            for i in range(10):
#                print ('RECV: ', DMXData[i],':')
#            break
#        if not DMXData:
#            break

DMXData.append(21)
DMXData.append(0)
DMXData.append(42)

        global wrapper
        wrapper = ClientWrapper()
        client = wrapper.Client()
  # send 1 dmx frame
        Universe = 1
        client.SendDmx(Universe, DMXData, DmxSent)
        wrapper.Run()

        
        self.request.send(b'ACK')

if __name__ == '__main__':
    serv = TCPServer(('', 20000), EchoHandler)
    print('Echo server running on port 20000')
    serv.serve_forever()
