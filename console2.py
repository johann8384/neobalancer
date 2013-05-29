#!/usr/bin/env python

from twisted.cred.portal import Portal
from twisted.conch.ssh.factory import SSHFactory
from twisted.internet import reactor
from twisted.conch.ssh.keys import Key
from twisted.cred.checkers import FilePasswordDB
from twisted.conch.interfaces import IConchUser
from twisted.conch.avatar import ConchUser
from zope.interface import implements

from twisted.python import log
import sys

log.startLogging(sys.stderr)

with open('id_rsa') as privateBlobFile:
    privateBlob = privateBlobFile.read()
    privateKey  = Key.fromString(data=privateBlob)

with open('id_rsa.pub') as publicBlobFile:
    publicBlob = publicBlobFile.read()
    publicKey  = Key.fromString(data=publicBlob)

class SSHAvatar(avatar.ConchUser):
    implements(conchinterfaces.ISession)

    def __init__(self, username, prompt):
        avatar.ConchUser.__init__(self)
        self.username = username
        self.prompt = prompt

        self.channelLookup.update({'session':session.SSHSession})

    def openShell(self, protocol):
        serverProtocol = insults.ServerProtocol(SSHProtocol, self, self.prompt)
        serverProtocol.makeConnection(protocol)
        protocol.makeConnection(session.wrapProtocol(serverProtocol))

    def getPty(self, terminal, windowSize, attrs):
        return None

    def execCommand(self, protocol, cmd):
        raise NotImplementedError

    def closed(self):
        pass
    
class SSHRealm:
    implements(portal.IRealm)

    def __init__(self, prompt):
        self.prompt = prompt
    
    def requestAvatar(self, avatarId, mind, *interfaces):
        if conchinterfaces.IConchUser in interfaces:
            return interfaces[0], SSHAvatar(avatarId, self.prompt), lambda: None
        else:
            raise Exception, "No supported interfaces found."

factory = SSHFactory()
factory.privateKeys = { 'ssh-rsa': privateKey }
factory.publicKeys  = { 'ssh-rsa': publicKey  }

factory.portal = Portal(SimpleRealm())
factory.portal.registerChecker(FilePasswordDB("ssh-passwords"))

reactor.listenTCP(2022, factory)
reactor.run()

