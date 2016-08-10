# vim:ts=4:sts=4:sw=4:expandtab

import bitstring as bs
import binascii as ba

class Parser(object):

	map_4b5b = {
		'0000': '0b11110',
		'0001': '0b01001',
		'0010': '0b10100',
		'0011': '0b10101',
		'0100': '0b01010',
		'0101': '0b01011',
		'0110': '0b01110',
		'0111': '0b01111',
		'1000': '0b10010',
		'1001': '0b10011',
		'1010': '0b10110',
		'1011': '0b10111',
		'1100': '0b11010',
		'1101': '0b11011',
		'1110': '0b11100',
		'1111': '0b11101'
	}

	map_5b4b = {
		'11110': '0b0000',
		'01001': '0b0001',
		'10100': '0b0010',
		'10101': '0b0011',
		'01010': '0b0100',
		'01011': '0b0101',
		'01110': '0b0110',
		'01111': '0b0111',
		'10010': '0b1000',
		'10011': '0b1001',
		'10110': '0b1010',
		'10111': '0b1011',
		'11010': '0b1100',
		'11011': '0b1101',
		'11100': '0b1110',
		'11101': '0b1111'
	}

	@classmethod
	def decode(cls, raw_data):
		# Shift out synchronization bits
		if raw_data[0] == 0:
			del raw_data[0]
		while raw_data[0:2] == '0b10':
			del raw_data[0:2]
		del raw_data[0:5]

		result = bs.BitArray()
		for pentabit in raw_data.cut(5):
			if pentabit.int == 0:
				break
			if pentabit.bin not in cls.map_5b4b:
				return (None, None, None)
			result += cls.map_5b4b[pentabit.bin]
		crc = result[-32:]
		del result[-32:]

		if ba.crc32(result.bytes) != crc.int:
			return (None, None, None)

		src_addr = result[:16]
		del result[:16]

		dest_addr = result[:16]
		del result[:16]

		msg = result

		return (src_addr, dest_addr, str(msg.bytes))

	@classmethod
	def encode(cls, src_addr, dest_addr, msg):
		result = bs.BitArray()
		chunk = bs.BitArray(src_addr, length=4) + bs.BitArray(dest_addr, length=4) + bs.BitArray(msg)
		crc = ba.crc32(chunk.bytes)
		chunk = chunk + bs.BitArray(int=crc, length=32)

		for halfbyte in chunk.cut(4):
			result += cls.map_4b5b[halfbyte.bin]

		return result
