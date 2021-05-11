### Converts string to its int representation.
# For each character as utf-8 gets its bits
# representation and forms a number
#
# @type s:      str
# @param s:     string to be converted
# @rtype:       int
# @return:      int representation of s
###
def str_as_int(s):
    if s == '':
        return 0
    num = 0
    for i in range(len(s)):
        num <<= 8
        num |= ord(s[i])
    return num


### Converts integer to its string representation.
# For each 8 bits gets its utf-8
# representation and forms a string

# @type num:      int
# @param num:     integer to be converted
# @rtype:         str
# @return:        string representation of num
###
def int_as_str(num):
    s = ''
    mask = 0xff
    i = 0
    l = num.bit_length()
    # starting from the lower bits
    # in order nit to miss leading zeros
    while i < l:
        s += chr(num & mask)
        num >>= 8
        i += 8
    return s[::-1]  # reversed string
