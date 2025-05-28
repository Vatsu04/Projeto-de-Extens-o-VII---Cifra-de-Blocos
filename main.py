import random
import math
import string 

chars = " " + string.punctuation + string.digits + string.ascii_letters + "áàâãäéèêëíìîïóòôõöúùûüçÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇ"
chars = list(chars)
key = chars.copy()

random.shuffle(key)

print(f"Chars: {chars}")
print(f"Key: {key}")

#ENCRYPTION 
plain_text = input("Enter the text to encrypt: ")
cipher_text = ""

for letter in plain_text:
    if letter in chars:
        index = chars.index(letter)
        cipher_text += key[index]
    else:
        print(f"Warning: Character '{letter}' not in chars list, skipping.")
        # Optionally: cipher_text += letter  # or another placeholder

print(f"Original menssage: {plain_text}")
print(f"encrypted message: {cipher_text}")

#EDECRYPTION
cipher_text = input("Enter the text to decrypt: ")
plain_text = ""

for letter in plain_text:
        index = chars.index(letter)
        cipher_text += chars[index]


print(f"Original menssage: {cipher_text}")
print(f"encrypted message: {plain_text}")

