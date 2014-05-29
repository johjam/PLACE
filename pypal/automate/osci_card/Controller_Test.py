'''
This module is an example where a simple measurement is taken after calling an optional initialization and dummy 
function. The dummy function doStuff can be replaced by any function that needs to be executed before the acquisition. 
For example, doStuff could move an element of an experimental setup to a certain position. When this is done the 
measurement is taken.

Command line options can be used to alter the behavior:

-r --sampleRate=
        define the sample rate. Attention only certain values are possible (check AlazarCmd.py). Supply an integer with
        suffix, e.g. 100K for 10e5 samples per second or 1M for 10e6 samples per second.
-c --channel=
        define the channel that shall be recorded. Example: -c A for channel A.
-d --duration=
        define the duration in seconds over which shall be recorded. Example: -n 5.5 to record 5.5 seconds.

FULL EXAMPLE 
python exampleAcquireInstancesAfterCommand.py -r 100K -c B --duration=10.


Created on Aug 14, 2013
@author: henrik
'''
'''
This module provides an examples how the osciCard module could be used. 

It acquires a certain number of records at moments when an external trigger signal rises over 0 V and displays the 
average of all records.

Command line options can be used to alter the behavior:

-r --sampleRate=
        define the sample rate. Attention only certain values are possible (check AlazarCmd.py). Supply an integer with
        suffix, e.g. 100K for 10e5 samples per second or 1M for 10e6 samples per second.
-c --channel=
        define the channel that shall be recorded. Example: -c A for channel A.
-n --numberOfRecords=
        define the number of records that shall be averaged. Example: -n 100 to average 100 records.

FULL EXAMPLE 
python exampleAverageMultipleRecords.py -r 100K -c B --numberOfRecords=10

@author: henrik
'''
'''
import osciCard.controller as card
import matplotlib.pyplot as plt 
import numpy as np
import sys
import getopt

def main():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:r:n:", ["help", "sampleRate=", "numberOfRecords=", "channel=" ])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # default values
    samplerate = "SAMPLE_RATE_100KSPS"
    averagedRecords = 50
    channel = "CHANNEL_A"
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        if o in ("-r", "--sampleRate"):
            samplerate = "SAMPLE_RATE_" + a + "SPS"
        if o in ("-n", "--numberOfRecords"):
            averagedRecords = int(a)
        if o in ("-c", "--channel"):
            channel = "CHANNEL_" + a
  
    initializeStuff()
    control = card.TriggeredContinuousController()  # get card handle
    control.configureMode = True  # go in configureMode; variables can be set without telling the card about it
    control.createInput(channel=channel)  # record on channel A
    control.setSampleRate(samplerate)  # record with 1e6 samples per second
    control.setTrigger(sourceOfJ="TRIG_EXTERNAL")  # use external signal for trigger
    control.setTriggerTimeout(0.1)  # set trigger time out
    control.setRecordsPerCapture(averagedRecords)
    control.configureMode = False  # leave configureMode; startCapture will run functions that configure the card
    doStuff()  # call dummy function
    control.startCapture()
    control.readData()
    times = control.getTimesOfRecord()  # get the time of each sample in one record
    records = control.getDataRecordWise(channel)  # get the data in a list of records
    records = np.array(records)
    average = np.average(records, 0) 
#    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(times, average)
    ax.set_ylabel("voltage [V]")
    ax.set_xlabel("time [s]")
    fig.canvas.set_window_title("Acquired Records Averaged")
    plt.show()

def initializeStuff():
    from XPS_C8_drivers import XPS
    global xps
    xps = XPS()
    xps.GetLibraryVersion()
    global socketId
    socketId = xps.TCP_ConnectToServer("130.216.54.129",5001,3)
#    socketId = xps.TCP_ConnectToServer("192.168.0.100",5001,100)
   # socketId = xps.OpenConnection(5001)
    print socketId
    print "connected to: ", socketId
    #print xps.CloseAllOtherSockets(socketId)
    xps.ControllerStatusGet(socketId)
    xps.Login(socketId, "Administrator", "Administrator")
    #print self.xps.GroupStatusListGet(self.socketId)
    print "Controller is initialized."
def doStuff():
     global xps
    #print self.xps.GroupKill(self.socketId, "GROUP3")
    #print self.xps.GroupInitialize(socketId, "GROUP3")
    #print self.xps.GroupStatusGet(socketId, "GROUP3")
    #print xps.GroupHomeSearch(socketId, "GROUP3")
    #print xps.GatheringConfigurationSet(socketId,["GROUP3.POSITIONER.CurrentPosition"])
    #print xps.GatheringRun(socketId, 1000, 100)
    #print xps.GroupHomeSearch(socketId, "GROUP3")
    #print xps.GroupJogParametersSet(socketId, "GROUP1", [0.05], [1.])
     print 'Jog Command sent'
     print xps.GroupMoveAbsolute(socketId, "GROUP3", [0.])
    #print xps.GatheringStopAndSave(socketId)
    #data= xps.GatheringDataGet(socketId, 1)
    #print xps.GatheringConfigurationGet(socketId)

if __name__ == '__main__':
    main()
'''


#Jami's Test
# --------- Python program: XPS controller demonstration --------
#
import XPS_C8_drivers
import sys
# Display error function: simplify error print out and closes socket
def displayErrorAndClose (socketId, errorCode, APIName):
    if (errorCode != -2) and (errorCode != -108):
        [errorCode2, errorString] = myxps.ErrorStringGet(socketId,errorCode)

        if (errorCode2 != 0):
            print APIName + ': ERROR ' + str(errorCode)
        else:
            print APIName + ': ' + errorString
    else:
        if (errorCode == -2):
            print APIName + ': TCP timeout'
        if (errorCode == -108):
            print APIName + ': The TCP/IP connection was closed by an administrator'
    myxps.TCP_CloseSocket(socketId)
    return

# Instantiate the class
myxps = XPS_C8_drivers.XPS()

# Connect to the XPS
socketId = myxps.TCP_ConnectToServer('192.168.0.254', 5001, 20)

# Check connection passed
if (socketId == -1):
    print 'Connection to XPS failed, check IP & Port'
    sys.exit ()

# Add here your personal codes, below for example:
# Define the positioner
group = 'XY'
positioner = group + '.X'

# Kill the group
[errorCode, returnString] = myxps.GroupKill(socketId, group)
if (errorCode != 0):
    displayErrorAndClose (socketId, errorCode, 'GroupKill')
    sys.exit ()

# Initialize the group
[errorCode, returnString] = myxps.GroupInitialize(socketId,group)
if (errorCode != 0):
    displayErrorAndClose (socketId, errorCode, 'GroupInitialize')
    sys.exit ()

# Home search
[errorCode, returnString] = myxps.GroupHomeSearch(socketId,
group)
if (errorCode != 0):
    displayErrorAndClose (socketId, errorCode, 'GroupHomeSearch')
    exit
# Make some moves
for index in range(10):
    # Forward
    [errorCode, returnString] = myxps.GroupMoveAbsolute(socketId,positioner, [20.0])
    if (errorCode != 0):
        displayErrorAndClose (socketId, errorCode,'GroupMoveAbsolute')
        sys.exit ()

# Get current position
[errorCode, currentPosition] = myxps.GroupPositionCurrentGet(socketId, positioner, 1)
if (errorCode != 0):
    displayErrorAndClose (socketId, errorCode,'GroupPositionCurrentGet')
    sys.exit ()
else:
    print 'Positioner ' + positioner + ' is in position ' + str(currentPosition)

# Backward
[errorCode, returnString] = myxps.GroupMoveAbsolute(socketId,
positioner, [-20.0])
if (errorCode != 0):
    displayErrorAndClose (socketId, errorCode,'GroupMoveAbsolute')
    sys.exit ()

# Get current position
[errorCode, currentPosition] = myxps.GroupPositionCurrentGet(socketId, positioner, 1)
if (errorCode != 0):
    displayErrorAndClose (socketId, errorCode,'GroupPositionCurrentGet')
    sys.exit ()
else:
    print 'Positioner ' + positioner + ' is in position ' + str(currentPosition)
# Close connection
myxps.TCP_CloseSocket(socketId)
#----------- End of the demo program ----------#