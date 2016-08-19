# audio-modem
Audio modem developed as an project assignment for Computer networking course.
This program is capable of transmitting strings between two computers using a simple headset or an audio cable.

##Technical details
Here's a simple diagram describing the radio stack from the transmitter's perspective.

```
                +------------------+
                | Sync. invocation +-+
                +------------------+ |
+----------+    +----------------+   | +-----------------+
|   Data   +--+->  4B5B encoding +----->01010001001001010|
+----------+  | +----------------+   | +--------+--------+
+----------+  | +----------------+   |          |
|  Address +--+ | Trailing zeros +---+          |
+----------+    +----------------+     +--------v---------+
                                       | Freq. modulation |
                                       +--------+---------+
                                                |
                                         +------v-------+
                                         | Audio output |
                                         +--------------+
```
	 
##Instructions
* Install all python dependencies with `pip install -r requirements.txt`
* Run receiver.py and type in a 2-byte host address (eg. 0x0001)

```
############################
# RECEIVER                 #
############################
Type host address (eg. 0xABCD): 0x0001
```

* In another terminal session, run play.py and type in a 2-byte host address (eg. 0x0002) 

```
############################
# PLAYER                   #
############################
Type host address (eg. 0xABCD): 0x0002
```

* Now you're able to type in the receiver's address as well as the message to be sent.

```
Type dest address (eg. 0xABCD): 0x0001
Type message (eg. Hello World!): Test test test
------BINARY OUTPUT START-------
10101010101010101010101010101010101010101010101010101010101010100000011110111101111010100111101111011110010010101101010011100101101111101010111101010101001111001111010100111001011011111010101111010101010011110011110101001110010110111110101011110101010101010110101110010111001110101111111010000000000000000
------BINARY OUTPUT END-------
```

