# 运行UDP协议，构建一个基于chord算法的p2p网络
# Author: 陈昊天
# Date: 2019-12-10
# Path: chord.py

import socket
import threading
import time
import random
import sys
import os
import hashlib
import json
import math
import struct
import binascii
import base64
import re
import copy
import queue
import datetime
import logging
import logging.handlers
import traceback
import argparse
import signal


# 用于存储节点信息的类
class Node:
    def __init__(self, ip, port, id):
        self.ip = ip
        self.port = port
        self.id = id

    def __str__(self):
        return 'ip: %s, port: %d, id: %d' % (self.ip, self.port, self.id)

    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return self.id != other.id
    
    def __lt__(self, other):
        return self.id < other.id
    
    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id
    
    def __ge__(self, other):
        return self.id >= other.id
    
    def __hash__(self):
        return hash(self.id)
    
    def __copy__(self):
        return Node(self.ip, self.port, self.id)
    
    def __deepcopy__(self, memo):
        return Node(self.ip, self.port, self.id)
    
    def __getstate__(self):
        return self.__dict__
    
    def __setstate__(self, state):
        self.__dict__.update(state)

# 用于存储文件信息的类
class File:
    def __init__(self, name, size, hash, node):
        self.name = name
        self.size = size
        self.hash = hash
        self.node = node

    def __str__(self):
        return 'name: %s, size: %d, hash: %s, node: %s' % (self.name, self.size, self.hash, self.node)

    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.hash == other.hash
    
    def __ne__(self, other):
        return self.hash != other.hash
    
    def __lt__(self, other):
        return self.hash < other.hash
    
    def __le__(self, other):
        return self.hash <= other.hash

    def __gt__(self, other):
        return self.hash > other.hash
    
    def __ge__(self, other):
        return self.hash >= other.hash
    
    def __hash__(self):
        return hash(self.hash)
    
    def __copy__(self):
        return File(self.name, self.size, self.hash, self.node)
    
    def __deepcopy__(self, memo):
        return File(self.name, self.size, self.hash, self.node)
    
    def __getstate__(self):
        return self.__dict__
    
    def __setstate__(self, state):
        self.__dict__.update(state)
    

# 用于存储文件块信息的类
class FileBlock:
    def __init__(self, name, size, hash, node, index):
        self.name = name
        self.size = size
        self.hash = hash
        self.node = node
        self.index = index

    def __str__(self):
        return 'name: %s, size: %d, hash: %s, node: %s, index: %d' % (self.name, self.size, self.hash, self.node, self.index)

    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.hash == other.hash
    
    def __ne__(self, other):
        return self.hash != other.hash
    
    def __lt__(self, other):
        return self.hash < other.hash
    
    def __le__(self, other):
        return self.hash <= other.hash

    def __gt__(self, other):
        return self.hash > other.hash
    
    def __ge__(self, other):
        return self.hash >= other.hash
    
    def __hash__(self):
        return hash(self.hash)
    
    def __copy__(self):
        return FileBlock(self.name, self.size, self.hash, self.node, self.index)
    
    def __deepcopy__(self, memo):
        return FileBlock(self.name, self.size, self.hash, self.node, self.index)
    
    def __getstate__(self):
        return self.__dict__
    
    def __setstate__(self, state):
        self.__dict__.update(state)






OPCODE = {
    'JOIN': 0,
    'JOIN_ACK': 1,
    'LEAVE': 2,
    'LEAVE_ACK': 3,
    'FIND_SUCCESSOR': 4,
    'FIND_SUCCESSOR_ACK': 5,
    'FIND_PREDECESSOR': 6,
    'FIND_PREDECESSOR_ACK': 7,
    'NOTIFY': 8,
    'NOTIFY_ACK': 9,
    'FIND_SUCCESSOR_LIST': 10,
    'FIND_SUCCESSOR_LIST_ACK': 11,
    'FIND_PREDECESSOR_LIST': 12,
    'FIND_PREDECESSOR_LIST_ACK': 13,
    'FIND_SUCCESSOR_LIST2': 14,
    'FIND_SUCCESSOR_LIST2_ACK': 15,
    'FIND_PREDECESSOR_LIST2': 16,
    'FIND_PREDECESSOR_LIST2_ACK': 17,
    'FIND_SUCCESSOR_LIST3': 18,
    'FIND_SUCCESSOR_LIST3_ACK': 19,
    'FIND_PREDECESSOR_LIST3': 20,
    'FIND_PREDECESSOR_LIST3_ACK': 21,
    'FIND_SUCCESSOR_LIST4': 22,
    'FIND_SUCCESSOR_LIST4_ACK': 23,
    'FIND_PREDECESSOR_LIST4': 24,
    'FIND_PREDECESSOR_LIST4_ACK': 25,
    'FIND_SUCCESSOR_LIST5': 26,
    'FIND_SUCCESSOR_LIST5_ACK': 27,
    'FIND_PREDECESSOR_LIST5': 28,
    'FIND_PREDECESSOR_LIST5_ACK': 29,
    'FIND_SUCCESSOR_LIST6': 30,
    'FIND_SUCCESSOR_LIST6_ACK': 31,
    'FIND_PREDECESSOR_LIST6': 32,
    'FIND_PREDECESSOR_LIST6_ACK': 33,
    'FIND_SUCCESSOR_LIST7': 34,
    'FIND_SUCCESSOR_LIST7_ACK': 35,
    'FIND_PREDECESSOR_LIST7': 36,
    'FIND_PREDECESSOR_LIST7_ACK': 37,
    'FIND_SUCCESSOR_LIST8': 38,
    'FIND_SUCCESSOR_LIST8_ACK': 39,
    'FIND_PREDECESSOR_LIST8': 40,
    'FIND_PREDECESSOR_LIST8_ACK': 41,
    'FIND_SUCCESSOR_LIST9': 42,
    'FIND_SUCCESSOR_LIST9_ACK': 43,
    'FIND_PREDECESSOR_LIST9': 44,
    'FIND_PREDECESSOR_LIST9_ACK': 45,
    'FIND_SUCCESSOR_LIST10': 46,
    'FIND_SUCCESSOR_LIST10_ACK': 47,
    'FIND_PREDECESSOR_LIST10': 48,
    'FIND_PREDECESSOR_LIST10_ACK': 49,
    'FIND_SUCCESSOR_LIST11': 50,
    'FIND_SUCCESSOR_LIST11_ACK': 51,
    'FIND_PREDECESSOR_LIST11': 52,
    'FIND_PREDECESSOR_LIST11_ACK': 53,
    'FIND_SUCCESSOR_LIST12': 54,
    'FIND_SUCCESSOR_LIST12_ACK': 55,
    'FIND_PREDECESSOR_LIST12': 56,
    'FIND_PREDECESSOR_LIST12_ACK': 57,
    'FIND_SUCCESSOR_LIST13': 58,
    'FIND_SUCCESSOR_LIST13_ACK': 59,
    'FIND_PREDECESSOR_LIST13': 60,
    'FIND_PREDECESSOR_LIST13_ACK': 61,
    'FIND_SUCCESSOR_LIST14': 62,
    'FIND_SUCCESSOR_LIST14_ACK': 63,
    'FIND_PREDECESSOR_LIST14': 64,
    'FIND_PREDECESSOR_LIST14_ACK': 65,
    'FIND_SUCCESSOR_LIST15': 66,
    'FIND_SUCCESSOR_LIST15_ACK': 67,
    'FIND_PREDECESSOR_LIST15': 68,
    'FIND_PREDECESSOR_LIST15_ACK': 69,
    'FIND_SUCCESSOR_LIST16': 70,
    'FIND_SUCCESSOR_LIST16_ACK': 71,
    'FIND_PREDECESSOR_LIST16': 72,
    'FIND_PREDECESSOR_LIST16_ACK': 73,
    'FIND_SUCCESSOR_LIST17': 74,
    'FIND_SUCCESSOR_LIST17_ACK': 75,
    'FIND_PREDECESSOR_LIST17': 76,
    'FIND_PREDECESSOR_LIST17_ACK': 77,
    'FIND_SUCCESSOR_LIST18': 78,
    'FIND_SUCCESSOR_LIST18_ACK': 79,
    'FIND_PREDECESSOR_LIST18': 80,
    'FIND_PREDECESSOR_LIST18_ACK': 81,
    'FIND_SUCCESSOR_LIST19': 82,
    'FIND_SUCCESSOR_LIST19_ACK': 83,
    'FIND_PREDECESSOR_LIST19': 84,
    'FIND_PREDECESSOR_LIST19_ACK': 85,
    'FIND_SUCCESSOR_LIST20': 86,
    'FIND_SUCCESSOR_LIST20_ACK': 87,
    'FIND_PREDECESSOR_LIST20': 88,
    'FIND_PREDECESSOR_LIST20_ACK': 89,
    'FIND_SUCCESSOR_LIST21': 90,
    'FIND_SUCCESSOR_LIST21_ACK': 91,
    'FIND_PREDECESSOR_LIST21': 92,
    'FIND_PREDECESSOR_LIST21_ACK': 93,
    'FIND_SUCCESSOR_LIST22': 94,
    'FIND_SUCCESSOR_LIST22_ACK': 95,
    'FIND_PREDECESSOR_LIST22': 96,
    'FIND_PREDECESSOR_LIST22_ACK': 97,
    'FIND_SUCCESSOR_LIST23': 98,
    'FIND_SUCCESSOR_LIST23_ACK': 99,
    'FIND_PREDECESSOR_LIST23': 100,
    'FIND_PREDECESSOR_LIST23_ACK': 101,
    'FIND_SUCCESSOR_LIST24': 102,
    'FIND_SUCCESSOR_LIST24_ACK': 103,


    
