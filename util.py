##
# Copyright (c) 2002-2004 ekit.com Inc (http://www.ekit-inc.com/)
# and Anthony Baxter <anthony@interlink.com.au>
# Copyright (c) 2007 Apple, Inc. (http://trac.calendarserver.org/),
# David Reid, and Wilfredo Sanchez
# Copyright (c) 2008 Divmod, Inc. (http://about.divmod.com/)
# and Duncan McGreggor <oubiwann@divmod.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
##

def boolify(data):
    """
    First, see if the data adheres to common string patterns for a boolean.
    Failing that, treat it like a reglar python object that needs to be checked
    for a truth value.
    """
    trues = ['yes', '1', 'on', 'enable', 'true']
    if isinstance(data, str) or isinstance(data, unicode):
        data = str(data)
        if data.lower() in trues:
            return True
        return False
    return bool(data)


def splitHostPort(hostPortString):
    """
    A utility needed for converting host:port string values in configuration
    files to a form that is actually useful.
    """
    hostPort = hostPortString.split(':')
    if len(hostPort) == 1:
        # this means no port was passed
        host = hostPort[0]
        port = 0
    else:
        host, port = hostPort
    port = int(port)
    if host == '*':
        host = ''
    return (host, port)
