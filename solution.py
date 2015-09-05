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

def rotate(l,n):
    return l[n:] + l[:n]

def decrypt_message(key, encrypted_message, first_index, last_index):
  num_encrypted_chars = len(encrypted_message)
  multiplier = num_encrypted_chars / (len(key)) + 1
  rotation = first_index % len(key)

  long_key = rotate(multiplier * key, rotation)[0: num_encrypted_chars]

  encrypted_word = encrypted_message[first_index:last_index]
  decrypted_word = [c ^ k for c,k in zip(encrypted_word,long_key)]
  word_candidate = ''.join([chr(x) for x in decrypted_word])

  return word_candidate

t0 = time.time()

english_words_list_link = 'http://www-01.sil.org/linguistics/wordlists/english/wordlist/wordsEn.txt'
cipher_text_file = 'p059_cipher.txt'

english_words = [word.strip() for word in set(urllib2.urlopen(english_words_list_link).read().split('\n'))]
encryped_chars = [int(i) for i in open(cipher_text_file, 'r').read().split(',')]

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

while True:
  message = decrypt_message(key, encryped_chars, 0, len(encryped_chars))
  words = message.split(' ')

  counter = collections.Counter(words)
  top_five = counter.most_common(5)

  top_five_availability = [word in english_words for (word, frequency) in top_five]

  if(all(top_five_availability)):
    print top_five
    break

  key = increment_and_wrap_key(key, ascii_a, ascii_z + 1)

message = decrypt_message(key, encryped_chars, 0, len(encryped_chars))
message_sum = sum(bytearray(message))

t1 = time.time()
delta_t = t1 - t0

print "EXECUTION TIME: {}".format(delta_t)
print "KEY: {}".format(key)
print "MESSAGE SUM: {}".format(message_sum)
print "MESSAGE: {}".format(message) 
