from typing import List
from math import isclose
from collections import Counter

####################### Descobrir o tamanho da chave - Indice de coinciencia #######################
with open('./texts/english.txt') as f:
    encrypted_text = f.read()
# Text
encrypted_text = encrypted_text.replace(" ", "").upper()

# Max number of key tests
max_key_size = 20

# Alphabet
alph = list(map(chr, range(ord('A'), ord('Z')+1)))

# Coincidende Indexes
# english_index = 0.0667
# portuguese_index = 0.0745

# 1 2 3 1 2 3, 2
# [[1, 1] [2, 2] ]


def split_text(encrypted_text: str, size: int) -> List[List[str]]:
    """Method responsible for splitting the encrypted text in different sizes to try finding out the key size.

    For instance: encrypted_text = "This is a test." and size = 2
    The return should be:  [['T', 'i', '', 's', 'a', 't', 's', '.'] ['h', 's', 'i', '', '', 'e', 't']]

    Args:
        encrypted_text (str): The encrypted text
        size (int): The number of times to split the text

    Returns:
        List[List[str]]: _description_
    """
    encrypted_chars = [*encrypted_text]
    splitted_texts = []
    for s in range(0, size):
        splitted_texts.append([encrypted_chars[i]
                              for i in range(s, len(encrypted_chars), size)])
    return splitted_texts


def getIOC(text: List[str]) -> float:
    """Calculates the index of coincidence of a text.

    Args:
        text (List[str]): A list containing all the chars of a text.

    Returns:
        float: The index of coincidence of the text.
    """
    N = len(text)
    # Returns a dict with letter as key and number of occurances as value
    freqs = Counter(text)
    freqsum = 0.0

    for letter in alph:
        freqsum += freqs[letter] * (freqs[letter] - 1)

    IC = freqsum / (N*(N-1))
    return IC


####################### Descobrir o tamanho da chave ########################
splitted_texts = []
key_size = -1
language = "undefined"
possible_key_sizes = []

for i in range(1, max_key_size):
    splitted_texts = split_text(encrypted_text, i)
    indexes_of_coincidence = []
    for text in splitted_texts:
        indexes_of_coincidence.append(getIOC(text))
    # Test indexes to check the length
    for index in indexes_of_coincidence:
        # if isclose(index, english_index, abs_tol=0.005):
        if index >= 0.0617 and index <= 0.0697:
            key_size = i
            language = "english"
            print("text is in english. Key Size = ", key_size)
            break
        # if isclose(index, portuguese_index, abs_tol=0.005):
        if index >= 0.0725 and index <= 0.082:
            key_size = i
            language = "portuguese"
            print("text is in portuguese. Key Size = ", key_size)
            break
    if language != "undefined" and key_size > 0:
        possible_key_sizes.append(key_size)

####################### Decifrar o texto #######################


# frequency analysis in each bin (we will find that each bin is just like the language frequency only shifted by a number. That number is the letter of the alphabet)
english_most_common_letters = ['E', 'A', 'I', 'N', 'O', 'S']
portuguese_most_common_letters = ['A', 'E', 'O', 'S', 'R', 'I']

import string

ALPHABET = string.ascii_uppercase

# Method to generate the Vigenere square
def generate_vigenere_square():
    vigenere_square = {}
    for i in range(len(ALPHABET)):
        shifted_alphabet = ALPHABET[i:] + ALPHABET[:i]
        vigenere_square[ALPHABET[i]] = shifted_alphabet
    return vigenere_square

# Method to decrypt the Vigenere cipher
def decrypt_vigenere(cipher_text, key_length):
    vigenere_square = generate_vigenere_square()
    segments = [cipher_text[i::key_length] for i in range(key_length)]
    decrypted_segments = []

    for segment in segments:
        # Determine the most common character in the segment
        counter = Counter(segment)
        most_common_char = counter.most_common(1)[0][0]

        # Calculate the shift amount for the segment
        shift_amount = ALPHABET.index(most_common_char) - ALPHABET.index('E')
        if shift_amount < 0:
            shift_amount += len(ALPHABET)

        # Decrypt the segment
        decrypted_segment = ''
        for i in range(len(segment)):
            key_char = ALPHABET[(i + ALPHABET.index(most_common_char)) % len(ALPHABET)]
            shifted_alphabet = vigenere_square[key_char]
            shifted_index = (ALPHABET.index(segment[i]) - ALPHABET.index(shifted_alphabet[shift_amount])) % len(ALPHABET)
            decrypted_segment += ALPHABET[shifted_index]

        decrypted_segments.append(decrypted_segment)

    # Combine the decrypted segments to get the original message
    decrypted_text = ''
    for i in range(len(cipher_text)):
        decrypted_text += decrypted_segments[i % key_length][i // key_length]

    return decrypted_text

print(decrypt_vigenere(encrypted_text, 7))

exit()

for key_size in possible_key_sizes:
    shifts_per_bin = []
    print("key size ", key_size)
    text_splitted_into_bins = split_text(encrypted_text, size=key_size)
    print("Text splitted bins ", len(text_splitted_into_bins))

    # A list of lists, where each inside list has a possible decripted bin
    possible_decripted_bins = []

    bin_number = 0
    for bin in text_splitted_into_bins:
        bin_number += 1
        possible_bin_decripted = []
        # Most frequent char in the bin:
        most_freq_char = ''
        biggest_occurance = 0
        for key, value in Counter(bin).items():
            if value > biggest_occurance:
                biggest_occurance = value
                most_freq_char = key
        # Difference between the most common and the possble letters it can be:
        possible_bin_shifts = []
        if language == "english":
            for l in english_most_common_letters:
                shift = abs(ord(most_freq_char) - ord(l)) - 1
                possible_bin_shifts.append(shift)
        if language == "portuguese":
            for l in portuguese_most_common_letters:
                shift = abs(ord(most_freq_char) - ord(l)) - 1
                possible_bin_shifts.append(shift)
        # Decript bin using the possile shifts

        print(f"Bin number {bin_number}: ", possible_bin_shifts)

        # Transform the bin (list) to text (str)
        # bin_text = ""
        # for l in bin:
        #     bin_text += l

        # # Make de shifts, decripting the bin for every possible shift
        # for shift in possible_bin_shifts:
        #     transformations = str.maketrans(
        #         alph, alph[-shift:] + alph[: -shift])
        #     decripted_bin_text = bin_text.translate(transformations)

        #     # Returning from str to list
        #     decripted_bin = []
        #     for l in decripted_bin_text:
        #         decripted_bin.append(l)

        #     possible_bin_decripted.append(decripted_bin)

        # possible_decripted_bins.append(possible_bin_decripted)

    # Combine the decrypted segments (possible_decripted_bins) to get the decrypted message.
    # for k in range(key_size):
    #     for possible_bin_decripted in possible_decripted_bins:
