
"""
This program allows you to sample data from a Pepwave Max HD4 modem
Here, the output is in a certain sim configuration but the program will work in any configuration, just make sure that the sims are in the right slot.
The program generates a new csv file in the same folder as this program every 1 min and writes the data.


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
import subprocess
from sys import stdout
from datetime import datetime
import paramiko, csv, os, re, time, socket, math


# Update the next three lines with your
# server's information

#TODO: DO NOT hardcode these parameters in the modules. Set these into variables in the 'main' module, or (even better),
#       set them in a seperate 'settings' file.
host = "192.168.50.1"
username = "admin"
password = ""
port = "8822"
MNO = ""
com = "get system"

def connectSSH():
    print ("Connecting to server via SSH...")
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=username, password=password, port=port)
    except:
        print ("Connecting not successfull.")
        return None
    Print("Success!")
    return client

def disconnectSSH(client):
    #will close the SSH connection
    print ("Closing the SSH connection...")
    client.close()
    return
    
def SSHgetData(client, command):
    #will execute a command in the SSH server. Will concat all return lines.
    print ("Executing command on server: '" + command + "'")
    try:
        stdin, stdout, stderr = client.exec_command(command)
    except:
        print ("Failed to execute command.")
        return ",,,"
    print("Success!")

    stdout=stdout.readlines()
    #TODO: show raw data in code comments. Usefull for unit testing and readability. 

    output=""
    for line in stdout:
        output=output+line

    return output

def parseData(data):
    #TODO: show raw data in code comments. Usefull for unit testing and readability. 
    print ("parsing data...")
    if "Connected" not in data:
        print ("Invalid data.")
        return ",,,"
    else:
        print (data)
        
    SINR = re.search('SINR                       : (.*)dB', data)
    RSRP = re.search('RSRP                       : (.*)dB', data)
    RSRQ = re.search('RSRQ                       : (.*)dB', data)
    conn = re.search('Network                    : (.*)\n', data)
    
    SINRres = SINR.group(1)
    RSRPres = RSRP.group(1)
    RSRQres = RSRQ.group(1)
    connres = conn.group(1)

    Signalstrength =  RSRQres + "," + RSRPres + "," + SINRres + ","  + connres
    
    return Signalstrength

def getData(client, com):
    data = SSHgetData(client, com)
    return parseData(data)

def getGPS():
    thePort = 60660
    #Function decimalToDM (Decimal to Degrees & Mins)
    #Convert the decimal-decimal degree value in the NEMA message to degrees and minutes
    #eg 5141.058053 (ddmm.mmmmmm) = 51 41.058053 = 51 + 41.058053/60 = 51.684301 degrees
    def decimalToDM( nemaIn ):
        #move decimal point for manipulation
        theDegrees= nemaIn / 100
        
        #create tuple of degrees and mins
        degsAndMins = math.modf(theDegrees)
        
        #Grab the Degrees as an integer
        theDegrees = int(degsAndMins[1]) 
        
        #restore original decimal point location
        theMins = degsAndMins[0] *100
        
        #grab the mins
        theMins=round(theMins,6)
        
        #convert decimal minutes to mins
        convertedMins=theMins/60
        
        #Add the degrees and mins together
        convertedResult=str(round(theDegrees + convertedMins,6))
        
        return convertedResult; 

    #Set up a client socket to connect to the GPS enabled device
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(5)
    #Connect to the device on the right Ip & port
    try:
        client_socket.connect((host, thePort))
    except socket.timeout:
        print("Can't connect to "+host+" on port "+str(thePort)+" : Timeout")
        quit()

    #Whilst we've received a response from the socket...
    data = client_socket.recv(1024)
    gps = "0,0"
    # make sure we actually have some data (and not just a response).
    if len(data) > 0:
        #decode the data from byte to string to make working with it easier
        print (data)
        thedata=data.decode('ascii')
        # split the data into a list of lines
        lines = thedata.splitlines(1)
        # iterate over each line
        for line in lines:
            #Data sent is coimma delimited so lets split it
            gpsstring = line.split(',')
            #if the first column contains $GPRMC and
            #if it has enough elements we have hit paydirt
            if gpsstring[0] == '$GPRMC' and len(gpsstring)>6:
                #check that there is returned GPS data
                if gpsstring[3]:
                    #Get Lat and Long String by converting decimals and adding compass pos
                    theLat = decimalToDM(float(gpsstring[3])) + (gpsstring[4])
                    theLong = decimalToDM(float(gpsstring[5])) + (gpsstring[6])
                    print ("Lat: " + theLat)
                    print ("Long: " + theLong)
                    
                    gps = theLat +","+ theLong
                    #Wait 5 secs 
                    time.sleep(5)           		
    return gps

def WriteToCSV():
    client = connectSSH()
    if client is None:
        return
    gps = getGPS()

    #TODO: DO NOT hardcode these parameters in the modules. Set these into variables in the 'main' module, or (even better),
    #       set them in a seperate 'settings' file.
    with open('modem.csv', 'w', newline='') as output_fn:
        timeStamp = datetime.now().strftime('%d-%m-%Y %H:%M')
        wr = csv.writer(output_fn, quoting=csv.QUOTE_NONE, escapechar=' ', delimiter= ',')
        print("writing to csv...")
        wr.writerow(["mno, RSRQ, RSRP, SINR, type, tijd, lat, long"]) 
        wr.writerow(["Vodafone", getData(client, "get wan 4"), timeStamp, gps])   
        wr.writerow(["T-Mobile", getData(client, "get wan 5"), timeStamp, gps]) 
        wr.writerow(["KPN", getData(client, "get wan 6"), timeStamp, gps]) 
        wr.writerow(["Tampnet", getData(client, "get wan 7"), timeStamp, gps]) 

    disconnectSSH(client)

def insertCSVtoDB:
    print("inserting CSV file into database...")
    subprocess.run(["psql",  "-f", "/home/cfns/systemtest/copymodem.sql", "postgres://postgres:stagecfns@localhost:5432/postgres"])

WriteToCSV()
insertCSVtoDB()