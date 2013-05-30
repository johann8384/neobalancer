# -*- test-case-name: src.test.test_main -*-

import datetime
import checker
from twisted.internet import reactor

class Compute(object):
    def add(self, a,b ):
        return a + b

class HealthCheck(object):
    self.checkType = 'ping'
    self.checkParameters = {}

    def __init__(self, checkType, checkParameters = {}):
        pass

    def executeCheck(self, host = ('127.0.0.1', '8080')):
        return True
    
#            d = ping(host, port)
#            d.addErrback(log.err)
#            d.addCallback(_makeGood, tracker, hostPort)
        

class Host(object):
    """
    This is a class for containing a specific host and trackng the connection information.

    @type hostName: string
    @param hostName: the name that the host  will be known by

    @type hostAddress: string
    @param hostAddress: the hostname or ip address for this host.

    @type service: string or list
    @param service: a string or list of strings of ports which represent the services provided by the host

    @type groupName: string
    @param groupName: the group that the host will be put into

    @type enabled: boolean or None
    @param enabled: a boolean that indicates whether the group for the host is
                    to be enabled, disabled, or ignored (None)
    """

    self.openconns = {}
    self.totalconns = {}
    self.lastclose = ''
    self.hostName = 'host01'
    self.hostAddress = '127.0.0.1'
    self.service = {}
    self.groupName = 'group01'
    self.enabled = True
    self.healthCheckPort = 80
    self.healthCheckInterval = 30

    def __init__(self, hostName = 'host01', hostAddress = '127.0.0.1', service = {'80', '4242'}, groupName = 'group01', healthCheckPort = 80, healthCheckInterval = 30):
        self.setHostName(hostName)
        self.setHostAddress(hostAddress)
        self.setService(service)
        self.healthCheckPort = healthCheckPort
        self.healthCheckInterval = healthCheckInterval
        self.startHealthCheck()
        pass

    def startHealthCheck(self):
        self.healthcheckID = reactor.callLater(self.healthCheckInterval, HealthCheck.executeCheck('ping', (self.hostAddress, self.healthCheckPort)))
        pass
    
    def cancelHealthCheck(self):
        self.healthcheckID.cancel()
        pass
    
    def getHostName(self):
        return self.hostName

    def setHostName(self, hostName):
        self.hostName = hostName
        return self.getHostName()

    def getHostAddress(self):
        return self.hostAddress

    def setHostAddress(self, hostAddress):
        self.hostAddress = hostAddress
        return self.getHostAddress()
    
    def getService(self):
        return self.service

    def setService(self, service):
        self.service = service
        return self.getService()

    def getGroupName(self):
        return self.groupName

    def setGroupName(self, groupName):
        self.groupName = groupName
        return self.getGroupName()
    
    def addConnection(self, connection, address = '127.0.0.1:80'):
        self.openconns[connection] = address
        self.totalconns[connection] = address
        pass
    
    def closeConn(self, connection):
        del self.openconns[connection]
        self.lastclose = datetime.now()
    
    def enable(self, enabled = True):
        self.enabled = enabled
        return self.isEnabled()

    def isEnabled(self):
        return self.enabled
    
    def getoOpenConns(self):
        return len(self.openconns)
    
    def getTotalConns(self):
        return len(self.totalconns)
    
    def getLastClose(self):
        return self.lastClose
    
    def resetHost(self):
        self.openconns = {}
        self.totalconns = {}
        self.lastclose = ''