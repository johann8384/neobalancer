import os

from twisted.python import log
from twisted.internet import defer
from twisted.internet import reactor
from twisted.internet import protocol

class PingProtocol(protocol.Protocol):
    """
    A simple protocol for doing nothing other than making a connection. Used in
    TCP pinging.
    """
    def connectionMade(self):
        self.factory.deferred.callback("success")
        self.factory.incrementCount()
        self.transport.loseConnection()


class PingFactory(protocol.ClientFactory):
    """
    The factory used when creating a "pinger."
    """
    protocol = PingProtocol

    def __init__(self):
        self.deferred = defer.Deferred()
        self.count = 0

    def clientConnectionFailed(self, connector, reason):
        self.deferred.errback(reason)

    def clientConnectionLost(self, connector, reason):
        pass

    def incrementCount(self):
        self.count += 1


def ping(host, port, tries=4, timeout=5):
    """

    """
    deferreds = []
    for i in xrange(tries):
        factory = PingFactory()
        reactor.connectTCP(host, port, factory, timeout=timeout)
        deferreds.append(factory.deferred)
    return defer.DeferredList(deferreds, consumeErrors=1)
