#!/usr/bin/env python
# vim:ts=4:sts=4:sw=4:expandtab

from transceiver import Receiver

print "############################"
print "# RECEIVER                 #"
print "############################"

addr = raw_input('Type host address (eg. 0xABCD): ')
rc = Receiver(addr, 200, 44100)

while True:
    (addr, msg) = rc.listen(addr)
    print "Received message from %s" % addr
    print msg
