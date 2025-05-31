import sys
import os

# ===============================
# INN SEGUROS - Cifra de Blocos 32 bits Simétrica
# ===============================

def pad_block(block, block_size=4):
    """Aplica padding ao bloco para garantir 4 bytes (32 bits)"""
    return block.ljust(block_size, b'\x00')

def read_blocks(filename, block_size=4):
    """Lê um arquivo binário em blocos de 4 bytes"""
    with open(filename, "rb") as f:
        while True:
            block = f.read(block_size)
            if not block:
                break
            if len(block) < block_size:
                block = pad_block(block, block_size)
            yield block

def write_blocks(filename, blocks):
    """Escreve blocos em um arquivo binário"""
    with open(filename, "wb") as f:
        for block in blocks:
            f.write(block)

def derive_subkeys(key):
    """
    Deriva 3 subchaves de 32 bits a partir da chave principal.
    Usa rotação e combinação para efeito avalanche.
    """
    subkeys = []
    for i in range(3):
        # Rotação circular à esquerda de i+1
        subkey = ((key << (i+1)) | (key >> (32 - (i+1)))) & 0xFFFFFFFF
        # Mistura bits (efeito avalanche)
        subkey ^= ((key >> ((i+1)*3)) | (key << (32-((i+1)*3)))) & 0xFFFFFFFF
        subkeys.append(subkey)
    return subkeys

def sbox(byte, key_byte):
    """
    Função S-BOX simples: substituição não linear dependente da chave
    """
    # Exemplo de S-Box: rotação + XOR + adição
    return ((byte ^ key_byte) + ((byte << 1) | (byte >> 7))) & 0xFF

def sbox_inv(byte, key_byte):
    """
    Inversa da função S-BOX para decriptação
    """
    # Desfaz a operação do S-Box acima
    tmp = (byte - ((byte << 1) | (byte >> 7))) & 0xFF
    return tmp ^ key_byte

def substitute(block_int, subkey):
    """
    Substituição byte a byte usando S-BOX dependente da subchave
    """
    out = 0
    for i in range(4):
        b = (block_int >> (8*(3-i))) & 0xFF
        k = (subkey >> (8*(3-i))) & 0xFF
        sb = sbox(b, k)
        out = (out << 8) | sb
    return out

def substitute_inv(block_int, subkey):
    """
    Inversa da substituição S-BOX
    """
    out = 0
    for i in range(4):
        b = (block_int >> (8*(3-i))) & 0xFF
        k = (subkey >> (8*(3-i))) & 0xFF
        sb = sbox_inv(b, k)
        out = (out << 8) | sb
    return out

def permute(block_int, subkey):
    """
    Permutação dos bits dependente da subchave
    Exemplo: embaralhamento dos nibbles (4 bits) baseado na subchave
    """
    positions = [(subkey >> (i*4)) & 0xF for i in range(8)]
    bits = [(block_int >> i) & 1 for i in range(32)]
    permuted = [0]*32
    for i in range(32):
        p = (i + positions[i % 8]) % 32
        permuted[p] = bits[i]
    out = 0
    for i in range(32):
        out |= (permuted[i] << i)
    return out

def permute_inv(block_int, subkey):
    """
    Inversa da permutação dos bits
    """
    positions = [(subkey >> (i*4)) & 0xF for i in range(8)]
    bits = [(block_int >> i) & 1 for i in range(32)]
    unpermuted = [0]*32
    for i in range(32):
        p = (i + positions[i % 8]) % 32
        unpermuted[i] = bits[p]
    out = 0
    for i in range(32):
        out |= (unpermuted[i] << i)
    return out

def encrypt_block(block_bytes, subkeys):
    """
    Realiza 3 rodadas de substituição e permutação para encriptar um bloco de 4 bytes
    """
    block = int.from_bytes(block_bytes, "big")
    for i in range(3):
        block = substitute(block, subkeys[i])
        block = permute(block, subkeys[i])
    return block.to_bytes(4, "big")

def decrypt_block(block_bytes, subkeys):
    """
    Realiza 3 rodadas de permutação e substituição inversas para decriptar um bloco de 4 bytes
    """
    block = int.from_bytes(block_bytes, "big")
    for i in reversed(range(3)):
        block = permute_inv(block, subkeys[i])
        block = substitute_inv(block, subkeys[i])
    return block.to_bytes(4, "big")

def process_file(input_file, output_file, key, mode="encrypt"):
    """
    Faz o processamento do arquivo inteiro em blocos de 32 bits
    """
    subkeys = derive_subkeys(key)
    processed_blocks = []
    for block in read_blocks(input_file):
        if mode == "encrypt":
            processed_blocks.append(encrypt_block(block, subkeys))
        else:
            processed_blocks.append(decrypt_block(block, subkeys))
    write_blocks(output_file, processed_blocks)

# ===============================
# Interface do Usuário
# ===============================
if __name__ == "__main__":
    print("=== INN Seguros - Cifra de Blocos 32 bits ===")
    mode = input("Escolha (E)ncriptar ou (D)ecriptar: ").strip().lower()
    # Entrada sempre na pasta 'Entrada'
    input_file_name = input("Nome do arquivo de entrada (dentro da pasta Entrada): ").strip()
    input_file = os.path.join("Entrada", input_file_name)

    # Saída sempre na pasta 'Saída'
    output_file_name = input("Nome do arquivo de saída (será criado na pasta Saída): ").strip()
    # Cria a pasta de saída se não existir
    os.makedirs("Saída", exist_ok=True)
    output_file = os.path.join("Saída", output_file_name)
    
    while True:
        key_str = input("Chave (8 dígitos hexadecimais, ex: 1a2b3c4d): ").strip()
        try:
            key = int(key_str, 16)
            if key < 0 or key > 0xFFFFFFFF:
                raise ValueError
            break
        except ValueError:
            print("Chave inválida! Use 8 dígitos hexadecimais.")
    
    process_file(input_file, output_file, key, mode="encrypt" if mode == "e" else "decrypt")
    print(f"Arquivo '{output_file}' gerado com sucesso!")