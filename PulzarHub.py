#!/usr/bin/env python
import mmap
import os
import struct
import time
import array

num_Frames = 100
Frame_Size = 512
Buffer_Size = Frame_Size * num_Frames

class fixed_size_frame_512(ctypes.Structure):
    _fields_ = [("data",ctypes.c_byte * 512)]


def main():
    # Open the file for reading
    fd = os.open('/tmp/DMX_Data', os.O_RDONLY)

    # Memory map the file
    buf = mmap.mmap(fd, Buffer_Size, mmap.MAP_SHARED, mmap.PROT_READ)
	
    frames = [memoryview(buf)[512*i : 512*(i+1)] for i in range(num_Frames)]

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
