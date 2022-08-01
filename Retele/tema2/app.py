import random
import socket
import hashlib
import os
import struct
import time

MAX_SIZE = 1 << 16


def make_sequence_number():
    return random.randint(3500, 59000) % (MAX_SIZE - 1)


def next_seq_num(seq_num,datalen = 1):
    return seq_num % (MAX_SIZE - 1) + datalen


SYN_flag = 0b10000000
SEQ_flag = 0b01000000
ACK_flag = 0b00100000
PSH_flag = 0b00010000
FIN_flag = 0b00001000
Packet_Size = 100

serverAddress = '127.0.0.1'
serverPort = 5005
server_address = (serverAddress, serverPort)


def create_header(flags, seq_num, ack_num=1, msg=''):
    header = struct.pack('!H', seq_num)
    header += struct.pack('!H', ack_num)
    header += struct.pack('B', flags)
    if msg != '':
        header += bytes(msg, 'utf-8')
    return header


def get_header_info(header):
    seq_num = int.from_bytes(header[:2], byteorder="big")
    ack_num = int.from_bytes(header[2:4], byteorder="big")
    flags = header[4]
    return seq_num, ack_num, flags

def get_message(header):
    return header[5:].decode('utf-8')