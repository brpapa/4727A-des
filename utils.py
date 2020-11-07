def hex2bin(s: str):
   """ 
   Hexadecimal to binary conversion 
   """
   # return bin(int(s, 16)).replace('0b', '')
   mp = {
      '0': "0000",
      '1': "0001",
      '2': "0010",
      '3': "0011",
      '4': "0100",
      '5': "0101",
      '6': "0110",
      '7': "0111",
      '8': "1000",
      '9': "1001",
      'A': "1010",
      'B': "1011",
      'C': "1100",
      'D': "1101",
      'E': "1110",
      'F': "1111"
   }
   binn = ""
   for i in range(len(s)):
      binn = binn + mp[s[i]]
   return binn


def bin2hex(s: str):
   """
   Binary to hexadecimal conversion
   """
   # return hex(int(s, 2)).replace('0x', '')

   mp = {
      "0000": '0',
      "0001": '1',
      "0010": '2',
      "0011": '3',
      "0100": '4',
      "0101": '5',
      "0110": '6',
      "0111": '7',
      "1000": '8',
      "1001": '9',
      "1010": 'A',
      "1011": 'B',
      "1100": 'C',
      "1101": 'D',
      "1110": 'E',
      "1111": 'F'
   }
   hexx = ""
   for i in range(0, len(s), 4):
      ch = ""
      ch = ch + s[i]
      ch = ch + s[i + 1]
      ch = ch + s[i + 2]
      ch = ch + s[i + 3]
      hexx = hexx + mp[ch]

   return hexx


def bin2dec(binary: int):
   """
   Binary to decimal conversion
   """

   binary1 = binary
   decimal, i, n = 0, 0, 0
   while(binary != 0):
      dec = binary % 10
      decimal = decimal + dec * pow(2, i)
      binary = binary//10
      i += 1
   return decimal


def dec2bin(num: int):
   """
   Decimal to binary conversion
   """

   res = bin(num).replace("0b", "")
   if(len(res) % 4 != 0):
      div = len(res) / 4
      div = int(div)
      counter = (4 * (div + 1)) - len(res)
      for i in range(0, counter):
         res = '0' + res
   return res
