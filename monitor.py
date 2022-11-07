import platform
import os
import time
from os.path import exists
import psutil
from datetime import datetime
import hashlib

#some const with the files names
SERCIVE_LIST = "serviceList.log"
STATUS_LOG = "Status_Log.log"
TEMP = "temp.txt"
TEMP2 = "tempserviceList.txt"
DATES = "date.txt"




class monitor:
    #init the monitor fields
    def __init__(self,slist=None, wo=None, stop=None,location=0):
        self.serviceDict = {}
        self.location=location
        self.listOfServices = []
        self.stop = False
        self.warning = []
        #delete old files
        if exists(SERCIVE_LIST):
            os.remove(SERCIVE_LIST)
        if exists(STATUS_LOG):
            os.remove(STATUS_LOG)
        if exists(DATES):
            os.remove(DATES)
    # method for monitoring in linux
    def linux(self):
        file = open(SERCIVE_LIST, 'a')
        if exists(TEMP2):
            os.remove(TEMP2)
        if exists(TEMP):
            os.remove(TEMP)
        file2 = open(DATES, 'a')
        #holds the value of the current time
        now = datetime.now()
        currTime = now.strftime("%Y/%m/%d %H:%M:%S")
        #holds the time and the current pos of the serviceList file
        sl = currTime + "~" + str(self.location)
        file2.write(sl + "\n")
      #  file.write("The time and date: ")
        os.system("date +%Y/%m/%d,%H:%M:%S >> {}".format(SERCIVE_LIST))
        #gets the updated status of all the running services in the operating system
        self.location = self.location + 1
        status = os.system("service --status-all | grep + >> {}".format(TEMP2))
        fileTemp = open(TEMP2, 'r')
        lines = fileTemp.readlines()
        file = open(SERCIVE_LIST, 'a')
        for line in lines:
             size1 = line.find("[", 1)
             service_status = "running"
             service_name = line[size1 + 7:len(line) - 1]
             s = service_name
             file.write(s + "\n")
             self.location=self.location+1
        file1 = open(STATUS_LOG, 'a')
        #gets the updated status of all the services
        os.system("service --status-all | grep + >> {}".format(TEMP))
        serviceHelp={}
        with open(TEMP) as file:
        #save each service name and status
         for line in file:
            size1 = line.find("[", 1)
            service_status = "running"
            service_name = line[size1 + 7:len(line) - 1]
            #if the service is new
            serviceHelp[service_name] = service_status
        for i, j in serviceHelp.items():
            if self.serviceDict.get(i)==None or self.serviceDict.get(i)=="stopped":
                self.serviceDict[i] = j
                s = j + ": " +i
                file1.write(s + "\n")
                self.listOfServices.append(s)
        for i, j in self.serviceDict.items():
            if serviceHelp.get(i) == None:
               if self.serviceDict.get(i) != "stopped":
                self.serviceDict[i] = "stopped"
                s = "stopped"+ ": " +i
                file1.write(s + "\n")
                self.listOfServices.append(s)

    #method for monitoring in windows
    def windows(self):
     file = open(SERCIVE_LIST, 'a')
     file1 = open(STATUS_LOG, 'a')
     file2 = open(DATES, 'a')
     #holds the current time and insert it into the file
     now = datetime.now()
     currTime = now.strftime("%Y/%m/%d %H:%M:%S")
     sl = currTime + "~" + str(self.location)
     file2.write(sl + "\n")
     # file2.write(sl + "\n")
     file.write(currTime+"\n")
     self.location = self.location + 1
     #iterate over all the services
     for service in psutil.win_service_iter():
        service_name = service.name()
        service_status = service.status()
        #if there's any new service -> write it into status_Log
        if self.serviceDict.get(service_name) == None:
            s = service_status + ": " + service_name
            file1.write(s + "\n")
            self.listOfServices.append(s)

        else:
            sta = self.serviceDict[service_name]
            # if there's any changes -> write it into status_Log
            if service_status != sta:
                s = service_status + ": " + service_name
                file1.write(s + "\n")
                self.listOfServices.append(s)
        self.serviceDict[service_name] = service_status
        #write the running services into serviceList
        if service.status() == "running":
            # s = service_name+ "   |   " + service_status
            file.write(service_name + "\n")
            self.location=self.location+1

    #insert a commit number for file
    def commitFun(self, filename):
        BUF_SIZE = 65536  # read stuff in 64kb chunks!
        sha1 = hashlib.sha1()
        with open(filename, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha1.update(data)
        return sha1.hexdigest()

    #compare for updates between old file and new file- if there's a change it gets a
    # new commit word -> and print notification for changes
    def start(self,timeUnit):
        status = platform.system()  # print if window or linux
        while not self.stop:
            if (status == "Windows"):
                self.windows()
                commitFile1 = self.commitFun(SERCIVE_LIST)
                commitFile2 = self.commitFun(STATUS_LOG)
            else:
                self.linux()
                commitFile1 = self.commitFun(SERCIVE_LIST)
                commitFile2 = self.commitFun(STATUS_LOG)
            time.sleep(timeUnit)
            commitFile3 = self.commitFun(SERCIVE_LIST)
            commitFile4 = self.commitFun(STATUS_LOG)
            if commitFile1 != commitFile3:
                self.warning.append("The file is different")
            if commitFile2 != commitFile4:
                self.warning.append("The file is different")

    def stopMonitor(self):
        self.stop = True