from SocketServer import BaseRequestHandler, TCPServer

DMXData = bytearray(1024)

class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:
            DMXData = self.request.recv(1024)
            for i in range(10):
                print ('RECV: ', DMXData[i],':')
            break
#        if not DMXData:
#            break
        
        self.request.send(b'ACK')

if __name__ == '__main__':
    serv = TCPServer(('', 20000), EchoHandler)
    print('Echo server running on port 20000')
    serv.serve_forever()
