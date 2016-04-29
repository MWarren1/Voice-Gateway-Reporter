##############################
##  Voice Gateway Reporter  ##
##       Python 2.7         ##
##    By Redemption.Man     ##
##############################

import csv
import argparse
import os.path
import time

## CLI switches
parser = argparse.ArgumentParser(prog='gateway_reporter.py', description='Reports on the utilization of a sinlge gateway for every second for the length of the cdr file')
parser.add_argument('--input', required=True, help='CDR file input(must be csv)')
parser.add_argument('--gateway', required=True, help='IP address of gateway')
parser.add_argument('--channels', required=False, help='The number of channels on the gateway(optional)')

args = parser.parse_args()

## END of CLI switches
## start of timer
starttime = time.time()
print "Started at "+str(starttime)
## Var's that can be changed
parsedoutputfile = "Parsed_CDR_" + args.gateway + ".csv"
outputfile = "Gateway_Report_" + args.gateway + ".csv"

## arg.input is the input file
gateway = args.gateway

#create parsed output cvs 
parsedoutput = open(parsedoutputfile, 'w+')
parsedoutput.write("globalCallID_callId,dateTimeOrigination,Connection_Year,Connection_Month,Connection_Day,Connection_Hour,Connection_Min,Connection_Sec,dateTimeDisconnect,Disconnect_Year,Disconnect_Month,Disconnect_Day,Disconnect_Hour,Disconnect_Min,Disconnect_Sec,origDeviceName,destDeviceName\n")

## columns needed:
## starting at zero
## 2 - globalCallID_callId
## 4 - dateTimeOrigination
## 48 - dateTimeDisconnect
## 55 - Duration
## 56 - origDeviceName
## 57 - destDeviceName
#### Opens and parses cdr extracting only records with the gateway
maxduration = 0
firstrecord = 999999999999999
lastrecord = 0
with open(args.input, 'Ur') as f:
	print "Collecting all records for " + gateway + "\n\n"
	parserreader = csv.reader(f)
	for row in parserreader:
		if row[56] == gateway or row[57] == gateway:
			## finding longest call
			if maxduration <= int(row[55]):
				maxduration = int(row[55])
			## finding first call
			if int(row[4]) <= firstrecord:
				firstrecord = int(row[4])
			## finding last call
			if int(row[48]) >= lastrecord:
				lastrecord = int(row[48])
			## extracting call records
			dateTimeOrigination = time.localtime(float(row[4]))
			dateTimeDisconnect = time.localtime(float(row[48]))
			dateTimeOrigination_converted = str(dateTimeOrigination.tm_year) + "," + str(dateTimeOrigination.tm_mon) + "," + str(dateTimeOrigination.tm_mday) + "," + str(dateTimeOrigination.tm_hour) + "," + str(dateTimeOrigination.tm_min) + "," + str(dateTimeOrigination.tm_sec)
			dateTimeDisconnect_converted = str(dateTimeDisconnect.tm_year) + "," + str(dateTimeDisconnect.tm_mon) + "," + str(dateTimeDisconnect.tm_mday) + "," + str(dateTimeDisconnect.tm_hour) + "," + str(dateTimeDisconnect.tm_min) + "," + str(dateTimeDisconnect.tm_sec)
			parsedoutput.write(row[2] + "," + row[4] + "," + dateTimeOrigination_converted + "," + row[48] + "," + dateTimeDisconnect_converted + "," + row[56] + "," + row[57] + "\n")
 
parsedoutput.close()
f.close()
print "Collected all records :) \n\n"
#### Finished extracting data and close the parsed file
## 0 - globalCallID_callId
## 1 - dateTimeOrigination
## 2 - Connection_Year
## 3 - Connection_Month
## 4 - Connection_Day
## 5 - Connection_Hour
## 6 - Connection_Min
## 7 - Connection_Sec
## 8 - dateTimeDisconnect
## 9 - Disconnect_Year
## 10 - Disconnect_Month
## 11 - Disconnect_Day
## 12 - Disconnect_Hour
## 13 - Disconnect_Min
## 14 - Disconnect_Sec
## 15 - origDeviceName
## 16 - destDeviceName
input = parsedoutputfile

print "First Record : "+str(firstrecord)
print "Last Record : "+ str(lastrecord)
print "Longest Call was : "+str(maxduration)+" Seconds"

## START OF REPORTING
## create output csv file
output = open(outputfile, 'w+')
output.write("Date,Time,Channels in Use,Utilization(%)\n")
currenttime = firstrecord
if args.channels:
    checkutilization = "YES"
else:
	checkutilization = "NO"
## setup hour update
lasthour = 0
## open parsed file
with open(input, 'Ur') as g:
	reader = csv.reader(g)
	while currenttime <= lastrecord:
		channelsused = 0
		## makes sure your at the start of the file
		g.seek(0)
		## skips 1 row that has headings
		reader.next()
		durationcheck = maxduration + currenttime + 10
		
		for row in reader:
			## duration check to stop looping if passed call records to do with current time
			if int(row[1]) >= durationcheck:
				break				
			if int(row[1]) <= currenttime and int(row[8]) >= currenttime:
				if row[15] == gateway and row[16] == gateway:
					channelsused = channelsused + 2
				if row[15] == gateway and row[16] != gateway:
					channelsused = channelsused + 1
				if row[15] != gateway and row[16] == gateway:
					channelsused = channelsused + 1
		## preparing and writing output of that second to file
		convertcurrenttime = time.localtime(float(currenttime))
		reportdate = str(convertcurrenttime.tm_year) + "/" + str(convertcurrenttime.tm_mon) + "/" + str(convertcurrenttime.tm_mday)
		reporttime = str(convertcurrenttime.tm_hour) + ":" + str(convertcurrenttime.tm_min) + ":" + str(convertcurrenttime.tm_sec)
		if checkutilization == "YES":
			
			utilization = (float(channelsused)/int(args.channels))*100
			utilization = format(utilization, '.0f')
		else:
			utilization = "N/A"
		output.write(reportdate+","+reporttime+","+str(channelsused)+","+str(utilization)+"\n")
		## prints update every hour of the report it completes
		if lasthour != str(convertcurrenttime.tm_hour):
			print "now reporting on "+ reportdate+" hour "+str(convertcurrenttime.tm_hour)
			lasthour = str(convertcurrenttime.tm_hour)
		currenttime = currenttime + 1
	
## Closing output file
g.close()
## last bit of timer
finishtime = time.time()
totaltime = finishtime - starttime
print "Finish at "+str(finishtime)
print str(totaltime) + " Seconds to complete report"