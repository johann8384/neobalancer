#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
from twisted.internet import protocol
from twisted.internet import reactor
import re

class MyPP(protocol.ProcessProtocol):
    def __init__(self, verses):
        self.verses = verses
        self.data = ""
        
    def connectionMade(self):
        print "connectionMade!"
        self.transport.writeToChild(0, "Aleph-null bottles of beer on the wall,\n" +
                             "Aleph-null bottles of beer,\n" +
                             "Take one down and pass it around,\n" +
                             "Aleph-null bottles of beer on the wall.\n")
        self.transport.closeChildFD(0)

    def childDataReceived(self, childFD, data):
        if childFD == 1:
            print "outReceived! with %d bytes!" % len(data)
            self.data = self.data + data
        if childFD == 2:
            print "errReceived! with %d bytes!" % len(data)
            print data

    def errConnectionLost(self):
        print "errConnectionLost! The child closed their stderr."

    def processExited(self, reason):
        print "processExited, status %d" % (reason.value.exitCode,)

    def processEnded(self, reason):
        print "processEnded, status %d" % (reason.value.exitCode,)
        print "quitting"
        reactor.stop()
        
def main():
    pp = MyPP(10)
    reactor.spawnProcess(pp, "./console.py", ["./console.py"], env=None, childFDs = {0: "w", 1: "r", 2:"r"})
    reactor.run()

main()
