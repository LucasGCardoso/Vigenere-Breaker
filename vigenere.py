from typing import List
from math import isclose
from collections import Counter
import sys
import string

# Alphabet vector starting from A until Z
ALPHABET = string.ascii_uppercase


def main():
    print("Starting parameters...")
    # starting parameters
    # Max number of key tests
    max_key_size = 20
    if len(sys.argv) <= 1:
        print("Missing arguments. Exiting. Usage: vigenere.py path/to/file.text")
        exit()
    # Encrypted text from file
    encrypted_text = read_encrypted_file(file_path=sys.argv[1])
    # Text decoded
    plain_text = ""

    print("Breaking Vigenere Cypher...")
    # Starting
    # Finding possible key lengths
    possible_key_lengths, language = find_key_length_and_language(
        max_key_size, encrypted_text)
    print(f"Language: ", language)
    # Finding possible keys
    possible_keys = list(
        set(find_key(possible_key_lengths, language, encrypted_text)))

    # User prompt
    invalid_prompt = True
    while (invalid_prompt):
        print("Please select the key you want to use to decrypt the text, using the number options: ")
        for i in range(0, len(possible_keys)):
            print(f'{i} - {possible_keys[i]}')
        key_index = input("Please enter the number of the key: ")

        # Validating user prompt
        try:
            key_index = int(key_index)
            invalid_prompt = False
        except Exception:
            invalid_prompt = True

        if invalid_prompt:
            continue
        if key_index >= len(possible_keys) or key_index < 0:
            invalid_prompt = True
        else:
            invalid_prompt = False

    plain_text = decrypt_vigenere(
        possible_keys[int(key_index)], encrypted_text)
    print("Writing file with plain text...")
    # open text file
    text_file = open("decoded_text.txt", "w")

    # write string to file
    text_file.write(plain_text)

    # close file
    text_file.close()
    print("Done!")


def decrypt_vigenere(key: str = "", encrypted_text: str = "") -> str:
    print(f'Decoding using key: ', key)
    ######## Descriptografar o texto usando a chave encontrada #########
    key_length = len(key)
    plain_text = ''

    # Decrypt the ciphertext using the computed key
    for i in range(len(encrypted_text)):
        ciphertext_char = encrypted_text[i]
        key_char = key[i % key_length]
        plain_char = ALPHABET[(ALPHABET.index(
            ciphertext_char) - ALPHABET.index(key_char)) % 26]
        plain_text += plain_char

    return plain_text


def find_key(possible_key_lengths: list[int] = [7], language: str = 'english', cipher_text: str = "") -> list[str]:
    print("Finding possible keys...")

    ########## Descobrindo a chave ##########
    most_frequent_letters = ['E', 'T', 'A']

    if (language == 'portuguese'):
        most_frequent_letters = ['A', 'E', 'O']

    possible_keys: list = []

    for key_length in possible_key_lengths:

        # Quebrando o texto cifrado em segmentos de tamanho:
        # seg[len(cipher_text) / key_length][key_length]
        segments = [cipher_text[i::key_length] for i in range(key_length)]

        # Olhando cada uma das colunas
        # vamos identificar qual é a letra mais frequente
        for language_most_frequent_letter in most_frequent_letters:
            key = ""
            for segment in segments:
                # Determine the most common character in the segment
                counter = Counter(segment)
                most_common_char = counter.most_common(1)[0][0]

                two_common_char = counter.most_common(2)
                # print(two_common_char)

                # agora determinamos qual é a letra da chave referente a coluna que estamos observando
                # Determine the key character by computing the distance to the most frequent letter
                key_distance = (ALPHABET.index(most_common_char) -
                                ALPHABET.index(language_most_frequent_letter)) % 26
                key += ALPHABET[key_distance]
            possible_keys.append(key)

    return possible_keys

# def find_key(possible_key_lengths:list[int]=[7], language:str='english', cipher_text:str="") -> list[str]:
    print("Finding possible keys...")

    ########## Descobrindo a chave ##########
    language_most_frequent_letters = ['A', 'E']

    if language == 'english':
        language_most_frequent_letters = ['E', 'T']

    possible_keys: list = []

    for key_length in possible_key_lengths:
        key = ""

        # Quebrando o texto cifrado em segmentos de tamanho:
        # seg[len(cipher_text) / key_length][key_length]
        segments = [cipher_text[i::key_length] for i in range(key_length)]

        # Olhando cada uma das colunas
        # vamos identificar qual é a letra mais frequente
        for segment in segments:
            # Determine the most common characters in the segment
            counter = Counter(segment)
            most_common_chars = [char for char,
                                 count in counter.most_common(2)]

            # Determine the key character by computing the distance to the most frequent letters
            key_distance_a = (ALPHABET.index(
                most_common_chars[0]) - ALPHABET.index(language_most_frequent_letters[0])) % 26
            key_distance_e = (ALPHABET.index(
                most_common_chars[1]) - ALPHABET.index(language_most_frequent_letters[1])) % 26

            # Determine which distance is closer to the expected value
            key_distance = key_distance_a
            if abs(key_distance_e - 5) < abs(key_distance_a - 5):
                key_distance = key_distance_e

            key += ALPHABET[key_distance]
        possible_keys.append(key)

    return possible_keys


def find_key_length_and_language(max_key_size: int = 20, encrypted_text: str = '') -> tuple[list[int], str]:
    print("Finding possible key lengths and language...")
    splitted_texts = []
    key_size = -1
    language = "undefined"
    possible_key_sizes = []

    for i in range(1, max_key_size):
        splitted_texts = split_text(encrypted_text, i)
        indexes_of_coincidence = []
        for text in splitted_texts:
            indexes_of_coincidence.append(get_IOC(text))
        # Test indexes to check the length
        for index in indexes_of_coincidence:
            if index >= 0.0617 and index <= 0.0697:
                key_size = i
                language = "english"
                print("text is in english. Key Size = ", key_size)
                break
            if index >= 0.0725 and index <= 0.082:
                key_size = i
                language = "portuguese"
                print("text is in portuguese. Key Size = ", key_size)
                break
        if language != "undefined" and key_size > 0:
            possible_key_sizes.append(key_size)

    return possible_key_sizes, language


def get_IOC(text: List[str]) -> float:
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

    for letter in ALPHABET:
        freqsum += freqs[letter] * (freqs[letter] - 1)

    IC = freqsum / (N*(N-1))
    return IC


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


def read_encrypted_file(file_path: str) -> str:
    with open(file_path) as f:
        encrypted_text = f.read()
    # Text
    encrypted_text = encrypted_text.replace(" ", "").upper()
    return encrypted_text


if __name__ == '__main__':
    main()
