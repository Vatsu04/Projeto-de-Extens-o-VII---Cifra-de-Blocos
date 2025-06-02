import os
import sys
from Funcoes.bloco_cipher import (
    pad_block, derive_subkeys, encrypt_block, decrypt_block
)

def process_text_file_encrypt(input_file, output_file, key):
    """
    Lê um arquivo TXT (plaintext); codifica em UTF-8 e o divide em blocos de 4 bytes,
    preenchendo o último bloco se necessário. Criptografa cada bloco, converte para
    string hexadecimal e grava em arquivo TXT.
    """
    subkeys = derive_subkeys(key)
    with open(input_file, "r", encoding="utf-8") as f:
        plaintext = f.read()
    data = plaintext.encode("utf-8")
    blocks = []
    for i in range(0, len(data), 4):
        block = data[i:i+4]
        if len(block) < 4:
            block = pad_block(block, 4)
        blocks.append(block)
    encrypted_blocks = [encrypt_block(block, subkeys) for block in blocks]
    encrypted_data = b"".join(encrypted_blocks)
    hex_string = encrypted_data.hex()
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(hex_string)
    print("Arquivo criptografado gerado com sucesso em:")
    print(output_file)

def process_text_file_decrypt(input_file, output_file, key):
    """
    Lê um arquivo TXT contendo a string hexadecimal (criptografada);
    converte para bytes, decripta bloco a bloco, remove padding e decodifica
    para UTF-8 antes de salvar em TXT.
    """
    subkeys = derive_subkeys(key)
    with open(input_file, "r", encoding="utf-8") as f:
        hex_string = f.read().strip()
    try:
        encrypted_data = bytes.fromhex(hex_string)
    except ValueError:
        print("Formato hexadecimal inválido no arquivo criptografado!")
        sys.exit(1)
    if len(encrypted_data) % 4 != 0:
        print("Conteúdo criptografado com tamanho inválido!")
        sys.exit(1)
    decrypted_blocks = []
    for i in range(0, len(encrypted_data), 4):
        block = encrypted_data[i:i+4]
        decrypted_blocks.append(decrypt_block(block, subkeys))
    if decrypted_blocks:
        decrypted_blocks[-1] = decrypted_blocks[-1].rstrip(b'\x00')
    decrypted_data = b"".join(decrypted_blocks)
    try:
        plaintext = decrypted_data.decode("utf-8")
    except UnicodeDecodeError:
        plaintext = decrypted_data.decode("latin1")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(plaintext)
    print("Arquivo descriptografado gerado com sucesso em:")
    print(output_file)

def criar_arquivo_interativo(diretorio, nome_arquivo):
    """
    Caso o arquivo (TXT) não exista, permite sua criação interativa.
    Garante que a extensão seja .txt.
    """
    print(f"O arquivo '{nome_arquivo}' não foi encontrado em '{diretorio}'.")
    escolha = input("Deseja criar este arquivo agora? (S/N): ").strip().lower()
    if escolha == "s":
        conteudo = input("Digite o conteúdo do arquivo (em uma linha ou cole o texto desejado):\n")
        if not nome_arquivo.lower().endswith('.txt'):
            nome_arquivo += ".txt"
        caminho = os.path.join(diretorio, nome_arquivo)
        os.makedirs(diretorio, exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)
        print(f"Arquivo '{caminho}' criado!")
        return caminho
    else:
        print("Operação cancelada pelo usuário.")
        sys.exit(1)