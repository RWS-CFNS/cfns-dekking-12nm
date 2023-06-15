# -*- coding: utf-8 -*-
"""
This program allows you to sample data from a Gill Maximet Weather station, type 'GMX500'
Here, the output is in a certain configuration but the program will work in any mode, just change the Copy.sql file accordingly.
The program generates a new text file in the same folder as this program every 1 min and writes the data.


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
#Library imports
import time
from datetime import datetime
from serial import *
 #TODO: do we need to import 'os'? As far as I can see, it is not used.
import os
import subprocess

#Serial paramaters
ser = Serial()        

#TODO: choose serial port dynamically: hardcoded port is not reliable (enough). Unix assigns the port on plugin of USB device.
#       check device name of each seial port to choose the correct one (for example using serial.tools.list_ports)
ser.port        = '/dev/ttyUSB0'                                                # choose serial port where device is plugged in
ser.baudrate    = 19200                                                         # default baud rate is 19200
ser.bytesize    = EIGHTBITS
ser.parity      = PARITY_NONE
ser.stopbits    = STOPBITS_ONE

#export file
fname = 'maximet.csv'

#TODO: factor out the serial operation, with error checking, catch timeout, etc.
# open serial 
ser.open()                                                                                                               

#read everything on the serial
rawdata = ser.readline()
#substring only the data and not start & ending chars
subdata = rawdata[1:36]
#TODO: show raw data in code comments. Usefull for unit testing and readability. 
#       Usually it is best to check the length of the data, and cut the first and last chars.
#       If length of data is less than 36 chars, last char is not cut.
#TODO: according to Maximet documentation, different serial communications can be used and several protocols. Please 
#       specify which are used.

#TODO: standard checksums are included in the data according to Maximet documentation. Add checksum compare to make 
#       sure data in intact, instead of cutting the checksum chars off.

#TODO: serial connection is never closed.



#TODO: factor out the file interactions 
#TODO: Why do we need to record the starttime? Variable is never used again.
#start timer
starttime = time.time()
#TODO: WHAT DOES THIS DO??? fname ('maximet.csv') is not a valid argument for strftime. filename will be exactly the same as fname.
filename = time.strftime(fname)
#TODO: this variable is never used again. Why do we need it?
fileInterval = 55

#Open fname and write substring to file    
#TODO: why open the file in binary mode?
fid = open(filename,'wb')
fid.write(subdata)
fid.close()

#TODO: WHY CLOSE THE FILE AND REOPEN IT ON THE NEXT LINE???    
#Open fname and write timestamp to file
fid = open(filename,'+a')
fid.write(',')
timeStamp = datetime.now().strftime('%d-%m-%Y %H:%M')
fid.write(timeStamp)
fid.close()



#print written data in console
print (subdata)
print (timeStamp)

#TODO: question: why do we need to write to csv and import that csv into the database seperately?
#       If there is a reason, document it properly. Else, create a (python) database interation module instead.
#TODO: DO NOT hardcode these parameters in the modules. Set these into variables in the 'main' module, or (even better),
#       set them in a seperate 'settings' file.
#run PostgreSQL command to copy th file to a database via commandline
subprocess.run(["psql", "-f", "/home/cfns/systemtest/copy.sql", "postgres://postgres:stagecfns@localhost:5432/postgres"])
