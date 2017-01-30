from telnetlib import *
import datetime
import os

#V1.2 - Added day by day folder sorting,
#       Added user name set to Backup Bot
#       Added more terminal feedback, with flag at server top.

# WARNING:
# Sensitive information is stored in this file (Serverquery login info)
# Ensure you remove this information, and keep the file secure.

#CONFIG - Find function calls at the bottom.
Output = 1
SortToFolder = 1

class PhysicalServer:
    def __init__(self, name, ip, port, user, serverpass):
        self.ServerName = name
        self.ServerIp = ip
        self.ServerPort = port
        self.ServerUser = user
        self.ServerPass = serverpass
        self.VirtualServers = []
        self.Login = "login " + self.ServerUser + " " + self.ServerPass + "\n"
        self.Login = self.Login.encode('ascii')
        if Output == 1:
            print("A new server has been created")
            print("Name: " + self.ServerName)
            print("Ip: " + self.ServerIp)

    # Retrive a list of all online servers.
    def GetActiveServers(self):
        if Output == 1:
            print("Attempting to obtain active servers...")
        Tn = Telnet(self.ServerIp, self.ServerPort, 10)
        Tn.open(self.ServerIp, self.ServerPort, 10)  # This might need to have the above brackets
        Tn.write(self.Login)
        Tn.read_until("error id=0 msg=ok".encode('ascii'))  # This is needed to move the read buffer forwards
        Tn.write("serverlist\n".encode('ascii'))
        serverlist = Tn.read_until("error id=0 msg=ok".encode('ascii'))
        Tn.close()
        serverlist = serverlist.split("|")
        serverlist[0] = serverlist[0][19:]
        for server in serverlist:
            ID = server.split(" ")[0].strip("virtualserver_id=")
            Port = server.split(" ")[1].strip("virtualserver_port=")
            Name = server.split(" ")[7].strip("virtualserver_name=").replace("\s"," ")
            self.VirtualServers.append(VirtualServer(ID,Port,Name))

    def BackupServers(self):
        Tn = Telnet(self.ServerIp, self.ServerPort, 10)
        Tn.open(self.ServerIp, self.ServerPort, 10)
        #Collecting backups
        for server in self.VirtualServers:
            Tn.write("use " + server.ID+"\n")
            Tn.read_until("error id=0 msg=ok")
            #Sets query name
            Tn.write("clientupdate client_nickname=Backup Bot\n")
            Tn.read_until("error id=0 msg=ok")
            #Take backup
            Tn.write(self.Login)
            Tn.read_until("error id=0 msg=ok")
            Tn.write("serversnapshotcreate\n")
            server.Snapshot = Tn.read_until("error id=0 msg=ok").replace("error id=0 msg=ok","")
            #Prints a message to the instance log
            logline = "logadd loglevel=4 logmsg=text This instance has been backed up."
            Tn.write(logline + "\n")
            Tn.read_until("error id=0 msg=ok")
            if Output == 1:
                print("Backed up " + server.Port)
        #Prints a message to the server log
        Tn.write("logout\n")
        Tn.write(self.Login)
        #Sets query name
        Tn.write("clientupdate client_nickname=Backup Bot\n")
        Tn.read_until("error id=0 msg=ok")
        logline = "logadd loglevel=4 logmsg=text Teamspeak virtual instance snapshots have been created."
        Tn.write(logline + "\n")
        Tn.close()

    def writeBackups(self):
            foldername = datetime.datetime.now().strftime("./%d-%m-%y/")
            if SortToFolder == 1:
                if not os.path.exists(os.path.dirname(foldername)):
                    os.makedirs(os.path.dirname(foldername))
                    if Output == 1:
                        print("A folder has been created for backups: " + foldername)
            for server in self.VirtualServers:
                filename = server.Name + " " + server.Port + " " + datetime.datetime.now().strftime("%d-%m-%y-%H-%M") + ".txt"
                if SortToFolder == 1:
                    os.chdir(foldername)
                backupFile = open(filename.replace("/","slash").replace("\\",""), "w")
                backupFile.write(server.Snapshot)
                backupFile.close()
                if Output == 1:
                    print("Backup written for port " + server.Port)
                if SortToFolder == 1:
                    os.chdir("..")

class VirtualServer:
    def __init__(self, Id, port, name):
        self.ID = Id
        self.Port = port
        self.Name = name
        self.Snapshot = ""
        if Output == 1:
            print("Virtual server found - ")
            print("Name: " + self.Name)
            print("Port: " + self.Port)

# WARNING:
# Sensitive information is stored in this file.
# Make sure you remove these before redistribution.
SovereignTs3 = PhysicalServer("TS NAME HERE","IP HERE","SQ PORT HERE","SQ USER HERE - Ensure you have the relevant permissions","SQ PASS HERE")
SovereignTs3.GetActiveServers()
SovereignTs3.BackupServers()
SovereignTs3.writeBackups()
