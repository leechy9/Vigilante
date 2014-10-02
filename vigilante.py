'''
Reads scrambled Vigenere Cipher text from stdin and attempts to decrypt it.
Written for Python 2.7.
Copyright (C) 2014 leechy9

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import string
from collections import defaultdict, Counter

# Average letter frequencies found in English (from Wikipedia)
letter_frequencies = [
  ('A', 0.08167),
  ('B', 0.01492),
  ('C', 0.02782),
  ('D', 0.04253),
  ('E', 0.12702),
  ('F', 0.02228),
  ('G', 0.02015),
  ('H', 0.06094),
  ('I', 0.06966),
  ('J', 0.00153),
  ('K', 0.00772),
  ('L', 0.04025),
  ('M', 0.02406),
  ('N', 0.06749),
  ('O', 0.07507),
  ('P', 0.01929),
  ('Q', 0.00095),
  ('R', 0.05987),
  ('S', 0.06327),
  ('T', 0.09056),
  ('U', 0.02758),
  ('V', 0.00978),
  ('W', 0.02360),
  ('X', 0.00150),
  ('Y', 0.01974),
  ('Z', 0.00074),
]

def all_substrings(text, size):
  '''Returns a list of all substrings with length of size in text'''
  length = len(text)
  return [text[i:i+size] for i in range(length) if i+size<=length]

def rotate_letter(letter, shift):
  '''Rotates the letter clockwise by the given shift value.'''
  rotated_letter = ord(letter) + shift
  if rotated_letter < ord('A'):
    rotated_letter = ord('Z') - (ord('A') - rotated_letter) + 1
  if rotated_letter > ord('Z'):
    rotated_letter = ord('A') + (rotated_letter - ord('Z')) - 1
  return chr(rotated_letter)
  

def calculate_distances(string_list):
  '''
  Takes in a list of strings and tells how far away matching elements are from
  one another. ['a','a'] has a distance of 1.
  Returns list((string, distance)).
  '''
  distances = []
  length = len(string_list)
  for i in range(length):
    for x in range(length):
      if string_list[i] == string_list[x] and i != x and i-x > 0:
        distances.append((string_list[i], i-x))
  return distances

def mod_counts(numbers, max_mod):
  '''
  Takes in a list(int). Calculates how many of the int%x==0 for 1<x<max_mod .
  Returns a defaultdict{mod, count} showing how many of the int%mod==0 .
  '''
  counts = defaultdict(int)
  for i in range(2, max_mod):
    for num in numbers:
      if num%i == 0:
        counts[i] += 1
  return counts

def find_shift_value(shift_column):
  '''
  Takes in a list of letters. Finds the most common occurrances.
  Uses these common occurrances to estimate how much the text was shifted.
  Returns a probable integer shift value.
  '''
  count = Counter(shift_column)
  # Ensure counts of 0 appear
  unfound_letters = [l for l in string.uppercase if l not in count]
  for l in unfound_letters: count[l] = 0
  total_letters = 0.0
  for l,c in count.most_common(): total_letters += c
  # Try to find the smallest difference between actual and expected frequencies
  differences = defaultdict(float)
  # Try shifting through every combination
  for r in range(len(letter_frequencies)):
    for l,f in letter_frequencies:
      rotated = rotate_letter(l, r)
      differences[r] += abs(f - count[rotated]/total_letters)
  # The smallest difference is most likely the shift value
  smallest = 0
  for s,d in differences.iteritems():
    if differences[s] < differences[smallest]:
      smallest = s
  return smallest

def vigenere_shift(text, shift_values):
  '''Rotates text by the shift_values given. Returns shifted value.'''
  key_length = len(shift_values)
  text = text.upper()
  shifted_letters = []
  for i in range(len(text)):
    rotated_letter = rotate_letter(text[i], -shift_values[i%key_length])
    shifted_letters.append(rotated_letter)
  return ''.join(shifted_letters)

def main():
  '''Main method'''
  cipher_text = raw_input('Enter the cipher text to decrypt: \n')
  print('Calculating...\n')
  substrings = all_substrings(cipher_text, 3)
  distances = calculate_distances(substrings)
  counts = mod_counts(zip(*distances)[1], 20)
  counts = [x for x in counts.iteritems()]
  counts.sort(key=lambda x: -x[1])
  # counts[x][0] should now contain key sizes from most to least probable
  key_size = counts[0][0]
  # Split letters by the key length and find the most common occurrences
  shift_values = []
  for i in range(key_size):
    shift_column = [cipher_text[x] for x in range(len(cipher_text)) if x%key_size==i]
    shift_values.append(find_shift_value(shift_column))
  decrypted_text = vigenere_shift(cipher_text, shift_values)
  print('\nExpected key: ')
  print(''.join([rotate_letter('A', c) for c in shift_values]))
  print('\nAlternative key (different starting shift sometimes encountered): ')
  print(''.join([rotate_letter('Z', c) for c in shift_values]))
  print('\nDecrypted text: ')
  print(decrypted_text)

# Call main method
if __name__ == '__main__':
  main()

