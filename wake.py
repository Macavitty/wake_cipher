from util import *


### Encapsulates WAKE algorithm.
# Attributes:
# INITIAL_KEY_SIZE_BYTES:   int
# S_BOX_SIZE:       int
# SBOX_AUXILIARY:   list
#                   initial s-box used for full s-box generation
# init_key:         int
#                   key provided by user
# s_box:            list
#                   substitution box with 256 entries of 32-bit words
# a_reg, b_reg,
# c_reg, d_reg:     int
#                   registers used for auto-key generation
#
# Methods:
# m(x, y):          mixing functions
# generate_sbox():  algorithm for generating s-box
# get_auto_key():   calculates auto-key in CFB cipher mode
# encrypt(char):    performs encryption
# decrypt(char):    performs decryption
###
class Wake:
    INITIAL_KEY_SIZE_BYTES = 16
    S_BOX_SIZE = 256
    SBOX_AUXILIARY = [
        0x726a8f3b, 0xe69a3b5c, 0xd3c71fe5, 0xab3c73d2,
        0x4d3a8eb3, 0x0396d6e8, 0x3d4c2f7a, 0x9ee27cf3
    ]

    def __init__(self, init_key):
        assert len(init_key) == self.INITIAL_KEY_SIZE_BYTES, \
            f'Could not perform WAKE: your key is {len(init_key)} bytes but must be {self.INITIAL_KEY_SIZE_BYTES} bytes'

        self.init_key = str_as_int(init_key)  # make int representation for further bitwise operation
        self.s_box = [0] * self.S_BOX_SIZE
        self.a_reg = self.b_reg = self.c_reg = self.d_reg = -1
        self.generate_sbox()

    def m(self, x, y):
        return (x + y) >> 8 ^ self.s_box[(x + y) & 255]

    def generate_sbox(self):
        mask = 0xffffffff  # 32 bits

        # fill first 4 boxes with initial key
        for i in range(4):
            self.s_box[i] = (self.init_key >> i * 32) & mask

        # fill other boxes in cycle
        for i in range(4, 256):
            x = self.s_box[i - 1] + self.s_box[i - 4]
            self.s_box[i] = x >> 3 ^ self.SBOX_AUXILIARY[x & 7]

        for i in range(23):
            self.s_box[i] += self.s_box[i + 89]

        # auxiliary variables
        x = self.s_box[33]
        z = self.s_box[59] | 0x01000001
        z &= 0xff7fffff
        x = (x & 0xff7fffff) + z

        # perform transposition in the 1st byte of all boxes
        for i in range(256):
            x = (x & 0xff7fffff) + z
            self.s_box[i] = self.s_box[i] & 0x00ffffff ^ x

        self.s_box[255] = self.s_box[0]
        x &= 255

        # shuffle boxes
        for i in range(256):
            ind = (self.s_box[i ^ x] ^ x) & 255
            self.s_box[i] = self.s_box[ind]
            self.s_box[x] = self.s_box[i]
        # finaly got cryptographically strong s-box

    def get_auto_key(self):
        if self.a_reg == -1:  # for the 1st character encryption/decryption
            mask = 0xffffffff
            self.a_reg = self.init_key & mask
            self.b_reg = (self.init_key >> 1 * 32) & mask
            self.c_reg = (self.init_key >> 2 * 32) & mask
            self.d_reg = (self.init_key >> 3 * 32) & mask
        else: # 4-cascade coding
            self.a_reg = self.m(self.a_reg, self.d_reg)
            self.b_reg = self.m(self.b_reg, self.a_reg)
            self.c_reg = self.m(self.c_reg, self.b_reg)
            self.d_reg = self.m(self.d_reg, self.c_reg)

        # new auto-key
        return self.d_reg

    def encrypt(self, char):
        # XOR cipher
        return int_as_str(str_as_int(char) ^ self.get_auto_key())

    def decrypt(self, char):
        # XOR cipher
        return int_as_str(str_as_int(char) ^ self.get_auto_key())
