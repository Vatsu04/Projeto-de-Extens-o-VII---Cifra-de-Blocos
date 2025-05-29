import random
import string
import itertools #Facilita o trabalho com grandes volumes de dados sem precisar armazenar tudo na memória.
import sys

# Definindo o alfabeto
chars = (
    " " + string.punctuation + string.digits + string.ascii_letters + "çáéíóúãõâêîôûäëïöüÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÑÒÓÔÕÖØÙÚÛÜÝÿ"
)
chars = list(chars)

# Gerando múltiplos substitutos para cada caractere
random.seed(42)  # Para reprodução, remova para produção
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
    # Para descriptografia
    for sub in possible_subs:
        if sub not in reverse_map:
            reverse_map[sub] = []
        reverse_map[sub].append(c)

# --- ENCRYPTION ---
def encrypt(text):
    cipher = ""
    for letter in text:
        if letter in sub_map:
            cipher += random.choice(sub_map[letter])
        else:
            cipher += letter
    return cipher

# --- DECRYPTION (printa todas até achar a correta) ---
def decrypt_bruteforce(ciphertext, original_word, max_results=10_000_000):
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

    if total_combinations > max_results:
        print("Muito grande para processar todas as combinações de uma vez. Tente um texto menor.")
        return

    for idx, candidate in enumerate(itertools.product(*possible_letters)):
        candidate_str = "".join(candidate)
        print(candidate_str)
        if candidate_str == original_word:
            print(f"\nPalavra original '{original_word}' encontrada na tentativa {idx+1}!")
            sys.exit(0)
    print("Palavra original não encontrada.")

# --- Exemplo de uso ---
if __name__ == "__main__":
    original_word = input("Digite o texto para encriptar: ")
    cipher_text = encrypt(original_word)
    print(f"Texto encriptado: {cipher_text}")

    print("\nTentando decriptar por força bruta (imprimindo todas as possibilidades):")
    decrypt_bruteforce(cipher_text, original_word)