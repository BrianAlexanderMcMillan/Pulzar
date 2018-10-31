from socket import socket, AF_INET, SOCK_STREAM
import array

DMXData = array.array('B')

for i in range(512):
    DMXData.append(0)

for i in range(4):
    ChanVal = raw_input("Channel, Value:").split(',')
    DMXData[int(ChanVal[0])-1] = int(ChanVal[1])

DMXData[0] = 48
DMXData[1] = 50
DMXData[2] = 80
DMXData[3] = 112

print DMXData

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 20000))

s.send(DMXData)

resp = s.recv(1024)
print('Response:', resp)

s.close()
