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
encryped_chars = [int(i) for i in open(cipher_text_file, 'r').read().split(',')]

# top 10 most common according to https://en.wikipedia.org/wiki/Most_common_words_in_English
english_words = set(['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have'])

ascii_space = 32
ascii_a = 97
ascii_z = 122

decrypted_message = []
key = [ascii_a, ascii_a, ascii_a]

ki = 0
last_i = 0
i = 0
num_valid_words = 0
char_regex = re.compile('[^a-zA-Z]')
num_encrypted_chars = len(encryped_chars)

while True:

  t0 = time.time()

  multiplier = num_encrypted_chars / (len(key))
  mod = num_encrypted_chars % len(key)
  long_key = multiplier * key + key[0:mod]

  print("A: {}".format(time.time() - t0))
  t0 = time.time()

  decrypted_word = [c ^ k for c,k in zip(encryped_chars,long_key)]
  message = ''.join([chr(x) for x in decrypted_word])
  words = [word.strip().lower() for word in message.split(' ')]

  print("B: {}".format(time.time() - t0))
  t0 = time.time()

  counter = collections.Counter(words)
  top_five = counter.keys()

  print("C: {}".format(time.time() - t0))

  if (len(set(top_five).intersection(english_words)) > 5):
    break

  t0 = time.time()

  key = increment_and_wrap_key(key, ascii_a, ascii_z + 1)

  print("D: {}".format(time.time() - t0))

message_sum = sum(bytearray(message))

t1 = time.time()
delta_t = t1 - t0

print "EXECUTION TIME: {}".format(delta_t)
print "KEY: {}".format(key)
print "MESSAGE SUM: {}".format(message_sum)
print "MESSAGE: {}".format(message) 
