#!python
#
# This is the server image that takes whatever it receives from clients and sends to the DMX driver
#
import mmap
import os
import struct
import time
import array

def main():
    # Open the file for reading
    fd = os.open('/tmp/DMX_Data', os.O_RDONLY)

    # Memory map the file
    buf = mmap.mmap(fd, mmap.PAGESIZE, mmap.MAP_SHARED, mmap.PROT_READ)

    i = None
    s = None
    data = array.array('B')

    for x in range(5): 
	data.append(x)

    while 1:
        new_i, = struct.unpack('i', buf[:4])
        new_s, = struct.unpack('3s', buf[4:7])

        if i != new_i or s != new_s:
            print 'i: %s => %d' % (i, new_i)
            print 's: %s => %s' % (s, new_s)
            print "1:", data[3], data[2] 
            print "2:", buf[42]
            print "3:", struct.unpack('B',buf[42])
            print 'Press Ctrl-C to exit'
            i = new_i
            s = new_s

        time.sleep(1)


if __name__ == '__main__':
    main()
