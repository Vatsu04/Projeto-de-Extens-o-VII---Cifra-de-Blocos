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

#Pode ser aqui o erro
def sbox(byte, key_byte):
    """
    Função S-BOX simples: substituição não linear dependente da chave
    """
    return ((byte ^ key_byte) + ((byte << 1) | (byte >> 7))) & 0xFF

#Pode ser aqui o erro
def sbox_inv(byte, key_byte):
    """
    Inversa da função S-BOX para decriptação
    """
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


#Pode ser aqui o erro
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
    positions = [(subkey >> (i*4)) & 0xF for i in range(8)]
    bits = [(block_int >> i) & 1 for i in range(32)]
    unpermuted = [0]*32
    for i in range(32):
        p = (i + positions[i % 8]) % 32
        unpermuted[i] = 0
    for i in range(32):
        p = (i + positions[i % 8]) % 32
        unpermuted[p] = bits[i]
    out = 0
    for i in range(32):
        out |= (unpermuted[i] << i)
    return out

def encrypt_block(block_bytes, subkeys):
    block = int.from_bytes(block_bytes, "big")
    for i in range(3):
        block = substitute(block, subkeys[i])
        block = permute(block, subkeys[i])
    return block.to_bytes(4, "big")

def decrypt_block(block_bytes, subkeys):
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

def criar_arquivo_interativo(diretorio, nome_arquivo):
    """
    Permite ao usuário criar um arquivo texto pelo terminal se ele não existir.
    """
    print(f"O arquivo '{nome_arquivo}' não foi encontrado em '{diretorio}'.")
    escolha = input("Deseja criar este arquivo agora? (S/N): ").strip().lower()
    if escolha == "s":
        conteudo = input("Digite o conteúdo do arquivo (tudo em uma linha, ou cole o texto desejado):\n")
        nome_txt = nome_arquivo
        # Garante extensão .txt
        if not nome_txt.lower().endswith('.txt'):
            nome_txt += ".txt"
        caminho = os.path.join(diretorio, nome_txt)
        os.makedirs(diretorio, exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)
        print(f"Arquivo '{caminho}' criado!")
        return caminho
    else:
        print("Operação cancelada pelo usuário.")
        sys.exit(1)

# ===============================
# Interface do Usuário
# ===============================
if __name__ == "__main__":
    print("=== INN Seguros - Cifra de Blocos 32 bits ===")
    mode = input("Escolha (E)ncriptar ou (D)ecriptar: ").strip().lower()

    if mode == "e":
        # ENCRIPTAR: entrada da pasta Descriptografado, saída na pasta Criptografado
        entrada_dir = "Descriptografado"
        saida_dir = "Criptografado"
        input_file_name = input("Nome do arquivo de entrada (dentro da pasta Descriptografado): ").strip()
        input_file = os.path.join(entrada_dir, input_file_name)
        if not os.path.isfile(input_file):
            input_file = criar_arquivo_interativo(entrada_dir, input_file_name)
        output_file_name = input("Nome do arquivo de saída (será criado na pasta Criptografado): ").strip()
        os.makedirs(saida_dir, exist_ok=True)
        output_file = os.path.join(saida_dir, output_file_name)
    else:
        # DECRIPTAR: entrada da pasta Criptografado, saída na pasta Descriptografado
        entrada_dir = "Criptografado"
        saida_dir = "Descriptografado"
        input_file_name = input("Nome do arquivo de entrada (dentro da pasta Criptografado): ").strip()
        input_file = os.path.join(entrada_dir, input_file_name)
        if not os.path.isfile(input_file):
            input_file = criar_arquivo_interativo(entrada_dir, input_file_name)
        output_file_name = input("Nome do arquivo de saída (será criado na pasta Descriptografado): ").strip()
        os.makedirs(saida_dir, exist_ok=True)
        output_file = os.path.join(saida_dir, output_file_name)
    
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