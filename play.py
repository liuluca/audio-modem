#!/usr/bin/env python
# vim:ts=4:sts=4:sw=4:expandtab

from transceiver import Transmitter

print "############################"
print "# PLAYER                   #"
print "############################"

addr = raw_input('Type host address (eg. 0xABCD): ')
tr = Transmitter(addr, 200, 44100, 10000)

while True:
	msg_addr = raw_input('Type dest address (eg. 0xABCD): ')
	msg = raw_input('Type message (eg. Hello World!): ')
	tr.send_message(msg_addr, msg)
