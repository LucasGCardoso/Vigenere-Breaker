from typing import List
from math import isclose

####################### Descobrir o tamanho da chave - Indice de coinciencia #######################
encrypted_text_example = ("CHREEVOAHMAERATBIAXXWTNXBEEOPHBSBQMQEQERBW"
                          "RVXUOAKXAOSXXWEAHBWGJMMQMNKGRFVGXWTRZXWIAK"
                          "LXFPSKAUTEMNDCMGTSXMXBTUIADNGMGPSRELXNJELX"
                          "VRVPPTULHDNQWTWDTYGBPHXTFALJHASVBFXNGLLCHR"
                          "ZBWELEKMSJIKNBHWRJGNMGJSGLXFEYPHAGNRBIEQJT"
                          "AMRVLCRREMNDGLXRRIMGNSNRWCHRQHAEYEVTAQEBBI"
                          "PEEWEVKAKOEWADREMXMTBHHCHRTKDNVRZCHRCLQOHP"
                          "WQAIIWXNRMGWOIIFKEE")
with open('./texts/english.txt') as f:
    encrypted_text = f.read()
# Text
encrypted_text = encrypted_text.replace(" ", "").lower()

# Max number of key tests
max_key_size = 20

# Alphabet
alph = "abcdefghijklmnopqrstuvwxyz"

# Coincidende Indexes
english_index = 0.0667
portuguese_index = 0.0745


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


def countLetters(text: str) -> int:
    """Counts the letters in the passed text.

    Args:
        text (str): The text to count the letters.

    Returns:
        int: The total number os letters (chars) the text has.
    """
    count = 0
    for i in text:
        count += 1
    return count


def getIOC(text: List[str]) -> float:
    """Calculates the index of coincidence of a text.

    Args:
        text (List[str]): A list containing all the chars of a text.

    Returns:
        float: The index of coincidence of the text.
    """
    letterCounts = []

    # Loop through each letter in the alphabet - count number of times it appears
    for i in range(len(alph)):
        count = 0
        for j in text:
            if j == alph[i]:
                count += 1
        letterCounts.append(count)

    # Loop through all letter counts, applying the calculation (the sigma part)
    total = 0
    for i in range(len(letterCounts)):
        ni = letterCounts[i]
        total += ni * (ni - 1)

    N = countLetters(text)
    c = 26.0  # Number of letters in the alphabet
    total = float(total) / ((N * (N - 1)))
    return total


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
        if isclose(index, english_index, abs_tol=0.005):
            key_size = i
            language = "english"
            print("text is in english. Key Size = ", key_size)
        if isclose(index, portuguese_index, abs_tol=0.005):
            key_size = i
            language = "portuguese"
            print("text is in portuguese. Key Size = ", key_size)
    print(indexes_of_coincidence)
    if language != "undefined" and key_size > 0:
        possible_key_sizes.append(key_size)
        language = "undefined"
        key_size = -1

# TODO
####################### Decifrar o texto #######################

# frequency analysis in each bin (we will find that each bin is just like the language frequency only shifted by a number. That number is the letter of the alphabet)
english_frequency = {
    'e': 12.0/100,
    't': 9.10/100,
    'a': 8.12/100,
    'o': 7.68/100,
    'i': 7.31/100,
    'n': 6.95/100,
    's': 6.28/100,
    'r': 6.02/100,
    'h': 5.92/100,
    'd': 4.32/100,
    'l': 3.98/100,
    'u': 2.88/100,
    'c': 2.71/100,
    'm': 2.61/100,
    'f': 2.30/100,
    'y': 2.11/100,
    'w': 2.09/100,
    'g': 2.03/100,
    'p': 1.82/100,
    'b': 1.49/100,
    'v': 1.11/100,
    'k': 0.69/100,
    'x': 0.17/100,
    'q': 0.11/100,
    'j': 0.10/100,
    'z': 0.07/100
}
char_frequencies = {}
for key_size in possible_key_sizes:
    text_splitted_into_bins = split_text(encrypted_text, size=key_size)
    for bin in text_splitted_into_bins:
        for char in bin:
            # Char frequency if does not exist
            if char not in char_frequencies.keys():
                count = 0
                for c in bin:
                    if char == c:
                        count += 1
                freq = float(count) / len(bin)
                char_frequencies[char] = freq
        print(char_frequencies)
        shifts = []
        for k, v in char_frequencies.items():
            for k_e, v_e in english_frequency.items():
                if isclose(v_e, v, abs_tol=0.005):
                    shifts.append(abs(ord(k) - ord(k_e)))
                    break
        print(shifts)
# Get the key (with the frequency analysis) and decipher it.
