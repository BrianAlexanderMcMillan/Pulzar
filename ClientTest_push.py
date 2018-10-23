from socket import socket, AF_INET, SOCK_STREAM
import array

DMXData = array.array('B')

for i in range(1024):
    DMXData[i] = 0;

DMXData[0] = 48
DMXData[1] = 50
DMXData[2] = 80
DMXData[3] = 112

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 20000))

s.send(DMXData)

resp = s.recv(1024)
print('Response:', resp)

s.close()
