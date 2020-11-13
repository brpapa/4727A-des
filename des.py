"""
   Data Encryption Standard (DES) algorithm.
"""
from utils import *
from constants import *

def f(right: str, subkey: str):
   assert(len(right) == 32 and len(subkey) == 48)

   # expand from 32 bits to 48 bits
   right_expanded = permute(right, expansion_table, 48)

   # xor between the 48-bit right and the 48-bit subkey of current round
   right = xor(right_expanded, subkey)

   # compress from 48 bits to 32 bits
   # transform each 6-bit group into a 4-bit group
   sbox = ""
   for i in range(8):
      group = right[i*6 : i*6+6]         # i-th group of 6 bits
      row = bin2dec(group[0] + group[5]) # row ranges 0 to 3 (00 to 11)
      col = bin2dec(group[1:5])          # col ranges 0 to 15 (0000 to 1111)
      val = sbox_tables[i][row][col]     # val ranges 0 to 15
      sbox = sbox + dec2bin(val)

   # permuting the bits
   return permute(sbox, straight_permutation_table, 32)

def encrypt(plain_text: str, subkeys: str):
   "Given a 64-bit plain text, encrypt it."

   assert(len(plain_text) == 64)

   # initial permutation
   plain_text = permute(plain_text, initial_permutation_table, 64)

   left = plain_text[0:32]
   right = plain_text[32:64]

   for round in range(16):
      previous_left = left
      left = right
      right = xor(previous_left, f(right, subkeys[round]))
      print("Round %2d:  L=%s  R=%s  K=%s" % (round+1, bin2hex(left), bin2hex(right), bin2hex(subkeys[round])))

   # swap
   left, right = right, left

   # final permutation
   cipher_text = permute(left + right, final_permutation_table, 64)
   return cipher_text

def generate_all_subkeys(key: str):
   "Compute all 16 48-bit subkeys, given a 64-bit key."
   assert(len(key) == 64)

   # getting 56-bit key from 64-bit original key using the parity bits
   key = permute(key, parity_bit_drop_table, 56)

   left = key[0:28]
   right = key[28:56]

   subkeys = []
   for round in range(16):
      left = shift_left(left, shift_table[round])
      right = shift_left(right, shift_table[round])

      # compression of key from 56 bits to 48 bits
      subkey = permute(left + right, key_transformation_table, 48)

      subkeys.append(subkey)

   return subkeys

if __name__ == "__main__":
   plain_text = hex2bin("0123456789ABCDEF") # 64-bit plain text
   key = hex2bin("133457799BBCDFF1")        # 64-bit key, but will be transformed into a 56-bit key

   subkeys = generate_all_subkeys(key)

   print("Encrypting...")
   print("Input (plain text):", bin2hex(plain_text))
   cipher_text = encrypt(plain_text, subkeys)
   print("Output (cipher text):", bin2hex(cipher_text))

   print("\nDecrypting...")
   print("Input (cipher text):", bin2hex(cipher_text))
   plain_text = encrypt(cipher_text, subkeys[::-1])
   print("Output (plain text):", bin2hex(plain_text))
