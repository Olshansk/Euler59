import io
import urllib2
import re
import time
import collections

def increment_and_wrap(curr_val, min_val, max_val):
  return min_val if curr_val + 1 >= max_val else curr_val + 1

def increment_and_wrap_key(curr_key, min_val, max_val):
  for i in xrange(len(curr_key)):
    curr_key[i] = increment_and_wrap(curr_key[i], min_val, max_val)
    if curr_key[i] != min_val:
      break
  return curr_key

t0 = time.time()

cipher_text_file = 'p059_cipher.txt'
cipher_text = [int(i) for i in open(cipher_text_file, 'r').read().split(',')]

# Top 10 most common according to https://en.wikipedia.org/wiki/Most_common_words_in_English
common_words = set(['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have'])

ascii_space = 32
ascii_a = 97
ascii_z = 122

key = [ascii_a, ascii_a, ascii_a]

# To meet the criteria of having this python program run in less than half a second,
# the divisor of the cipher text's length (4) was deduced emperically through trial and error.
#
# To generalize this solution to all cipher texts, and guarantee a solution, one can simply
# use the entire length of the provided cipher text.
#
# In the case of very long cipher texts, another approach is to nest the loop below inside
# another loop with the index starting at 1 and doubling on every iteration. Expontentially
# increasing the length being tested will approach the length of the original cipher text
# very rapidly, while only decrypting the shortest possible fragment of the encrypted text necessary.

cipher_text_length_to_decrypt = len(cipher_text) / 4
decrypted_message = [0 for x in xrange(cipher_text_length_to_decrypt)]

while True:

  for x in xrange(cipher_text_length_to_decrypt):
    decrypted_message[x] = chr(cipher_text[x] ^ key[x % 3])


  concated_message = ''.join(decrypted_message)
  
  words = [word.strip().lower() for word in concated_message.split(' ')]

  if (len(set(words).intersection(common_words)) > 5):
    break

  key = increment_and_wrap_key(key, ascii_a, ascii_z + 1)

# Get the whole decrypted message
full_decrypted_message = [0 for x in xrange(len(cipher_text))]
for x in xrange(len(cipher_text)):
  full_decrypted_message[x] = chr(cipher_text[x] ^ key[x % 3])
full_concated_message = ''.join(full_decrypted_message)
full_message_sum = sum(bytearray(full_decrypted_message))

t1 = time.time()
delta_t = t1 - t0

print "EXECUTION TIME: {}".format(delta_t)
print "KEY: {}".format(key)
print "MESSAGE SUM: {}".format(full_message_sum)
print "MESSAGE: {}".format(full_concated_message) 
