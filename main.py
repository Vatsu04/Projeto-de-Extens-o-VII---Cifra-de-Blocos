import random
import string
import itertools
import sys

try:
    from tqdm import tqdm  # Barra de progresso opcional
except ImportError:
    tqdm = lambda x, **kwargs: x  # Fallback se não tiver tqdm


# Definindo o alfabeto
chars = (
    " " + string.punctuation + string.digits + string.ascii_letters
)
chars = list(chars)

random.seed(42)
all_subs = chars.copy()
sub_map = {}
reverse_map = {}

for c in chars:
    possible_subs = []
    while len(possible_subs) < 2:
        s = random.choice(all_subs)
        if s not in possible_subs:
            possible_subs.append(s)
    sub_map[c] = possible_subs
    for sub in possible_subs:
        if sub not in reverse_map:
            reverse_map[sub] = []
        reverse_map[sub].append(c)

def encrypt(text):
    cipher = ""
    for letter in text:
        if letter in sub_map:
            cipher += random.choice(sub_map[letter])
        else:
            cipher += letter
    return cipher

def decrypt_bruteforce(ciphertext, original_word):
    possible_letters = []
    for c in ciphertext:
        if c in reverse_map:
            possible_letters.append(reverse_map[c])
        else:
            possible_letters.append([c])

    total_combinations = 1
    for choices in possible_letters:
        total_combinations *= len(choices)
    print(f"Total de combinações possíveis: {total_combinations}")

    # Barra de progresso (tqdm) opcional
    for idx, candidate in enumerate(tqdm(itertools.product(*possible_letters), total=total_combinations, desc="Processando")):
        candidate_str = "".join(candidate)
        print(candidate_str)
        if candidate_str == original_word:
            print(f"\nPalavra original '{original_word}' encontrada na tentativa {idx+1}!")
            sys.exit(0)
    print("Palavra original não encontrada.")

if __name__ == "__main__":
    original_word = input("Digite o texto para encriptar: ")
    cipher_text = encrypt(original_word)
    print(f"Texto encriptado: {cipher_text}")

    print("\nTentando decriptar por força bruta (demorado para textos grandes):")
    decrypt_bruteforce(cipher_text, original_word)