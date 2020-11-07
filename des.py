"""
   Data Encryption Standard (DES) algorithm.
"""
# TODO: continuar lendo: https://www.geeksforgeeks.org/data-encryption-standard-des-set-1/
# TODO: continuar lendo: http://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm
from utils import *
from constants import *

def permute(key, arr, n):
   """
   Permute function to rearrange the bits
   """

   permutation = ""
   for i in range(n):
      permutation += key[arr[i] - 1]
   return permutation

def shift_left(k, nth_shifts):
   """
   Shifting the bits towards left by nth shifts
   """

   s = ""
   for i in range(nth_shifts):
      for j in range(1,len(k)):
         s = s + k[j]
      s = s + k[0]
      k = s
      s = ""
   return k

def xor(a, b):
   """
   Calculating XOR of two strings of binary number a and b
   """

   ans = ""
   for i in range(len(a)):
      if a[i] == b[i]:
         ans = ans + "0"
      else:
         ans = ans + "1"
   return ans


def encrypt(plain_text, round_keys_bin, round_keys_hex):
   plain_text = hex2bin(plain_text)

   # Initial Permutation (1-based index)
   initial_permutation_table = [58, 50, 42, 34, 26, 18, 10, 2,
                                60, 52, 44, 36, 28, 20, 12, 4,
                                62, 54, 46, 38, 30, 22, 14, 6,
                                64, 56, 48, 40, 32, 24, 16, 8,
                                57, 49, 41, 33, 25, 17,  9, 1,
                                59, 51, 43, 35, 27, 19, 11, 3,
                                61, 53, 45, 37, 29, 21, 13, 5,
                                63, 55, 47, 39, 31, 23, 15, 7]
   plain_text = permute(plain_text, initial_permutation_table, 64)

   # Splitting
   left = plain_text[0:32]
   right = plain_text[32:64]

   # for each round r
   for r in range(0, 16):
      # Expansion D-box: Expanding the 32 bits data into 48 bits
      right_expanded = permute(right, exp_d, 48)

      # XOR RoundKey[r] and right_expanded
      xor_x = xor(right_expanded, round_keys_bin[r])

      # S-boxex: substituting the value from s-box table by calculating row and column
      sbox_str = ""
      for j in range(0, 8):
         row = bin2dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
         col = bin2dec(int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
         val = sbox[j][row][col]
         sbox_str = sbox_str + dec2bin(val)

      # Straight D-box: After substituting rearranging the bits
      sbox_str = permute(sbox_str, per, 32)

      # XOR left and sbox_str
      result = xor(left, sbox_str)
      left = result

      # Swapper
      if (r != 15): 
         left, right = right, left

      print("Round %2d: %s %s %s" % (r+1, bin2hex(left), bin2hex(right), round_keys_hex[r]))

   # Combination
   combine = left + right

   # Final permutaion: final rearranging of bits to get cipher text
   cipher_text = permute(combine, final_perm, 64)
   return cipher_text

# TODO: nao está lidando com um plaint_text com mais de 1 bloco de 64 bits
if __name__ == "__main__":

   # 64-bit plain text given as hex
   plain_text = "0123456789ABCDEF"  # must be multiple of 16 hex digits

   # 64-bit key given as hex, but will be transformed into a 56-bit key, so there is 2^56 = 72.057.594.037.927.936 key possibilities which it difficults brute force attacks
   key = "133457799BBCDFF1"

   # ---- GENERATE 16 SUBKEYS ---- #

   key = hex2bin(key)

   # getting 56-bit key from 64-bit original key using the parity bits
   # parity bit drop table
   # discarting the bits 8, 16, 24, 32, 40, 48, 56, 64 (1-based index)
   permutation_table = [57, 49, 41, 33, 25, 17,  9,
                         1, 58, 50, 42, 34, 26, 18,
                        10,  2, 59, 51, 43, 35, 27,
                        19, 11,  3, 60, 52, 44, 36,
                        63, 55, 47, 39, 31, 23, 15,
                         7, 62, 54, 46, 38, 30, 22,
                        14,  6, 61, 53, 45, 37, 29,
                        21, 13,  5, 28, 20, 12,  4]
   key = permute(key, permutation_table, 56)

   # splitting the key
   left = key[0:28]
   right = key[28:56]

   round_keys_bin = []
   round_keys_hex = []

   # number of bit shifts, for each round
   shift_table = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

   # for each round r
   for r in range(16):
      # shifting the bits of previous left and right
      left = shift_left(left, shift_table[r])
      right = shift_left(right, shift_table[r])

      # combination of left and right string
      combined = left + right

      # key transformation: generate a different 48-bit subkey from the 56-bit key
      # compression of key from 56 bits to 48 bits
      # discarting the bits 9, 18, 22, 25, 35, 38, 43, 54 (1-based index) 
      transformation_table = [14, 17, 11, 24,  1,  5,
                               3, 28, 15,  6, 21, 10,
                              23, 19, 12,  4, 26,  8,
                              16,  7, 27, 20, 13,  2,
                              41, 52, 31, 37, 47, 55,
                              30, 40, 51, 45, 33, 48,
                              44, 49, 39, 56, 34, 53,
                              46, 42, 50, 36, 29, 32]
      round_key = permute(combined, transformation_table, 48)

      round_keys_bin.append(round_key)
      round_keys_hex.append(bin2hex(round_key))

   # ---- RUN ENCRYPT AND DECRYPT ---- #

   print("Encryption:")
   print("Input (plain text):", plain_text)
   cipher_text = encrypt(plain_text, round_keys_bin, round_keys_hex)
   print("Output (cipher text):", bin2hex(cipher_text))

   print("")
   print("Decryption:")
   print("Input (cipher text):", bin2hex(cipher_text))
   plain_text = encrypt(bin2hex(cipher_text), round_keys_bin[::-1], round_keys_hex[::-1])
   print("Output (plain text):", bin2hex(plain_text))

