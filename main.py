import sys
import os

def pad_block(block, block_size=4):
    """Aplica padding para garantir 4 bytes (32 bits)."""
    return block.ljust(block_size, b'\x00')

def derive_subkeys(key):
    """
    Deriva 3 subchaves de 32 bits a partir da chave principal.
    Usa rotações e misturas para provocar efeito avalanche.
    """
    subkeys = []
    for i in range(3):
        subkey = ((key << (i + 1)) | (key >> (32 - (i + 1)))) & 0xFFFFFFFF
        subkey ^= ((key >> ((i + 1) * 3)) | (key << (32 - ((i + 1) * 3)))) & 0xFFFFFFFF
        subkeys.append(subkey)
    return subkeys

def sbox(byte, key_byte):
    """S-BOX simples e invertível: soma módulo 256."""
    return (byte + key_byte) & 0xFF

def sbox_inv(byte, key_byte):
    """Inversa da S-BOX: subtrai módulo 256."""
    return (byte - key_byte) & 0xFF

def substitute(block_int, subkey):
    """
    Aplica a substituição byte a byte usando a S-BOX dependente da subchave.
    Divide o inteiro em 4 bytes (ordem big‑endian) e refaz.
    """
    out = 0
    for i in range(4):
        b = (block_int >> (8 * (3 - i))) & 0xFF
        k = (subkey >> (8 * (3 - i))) & 0xFF
        sb = sbox(b, k)
        out = (out << 8) | sb
    return out

def substitute_inv(block_int, subkey):
    """
    Aplica a substituição inversa (S-BOX inversa) byte a byte.
    """
    out = 0
    for i in range(4):
        b = (block_int >> (8 * (3 - i))) & 0xFF
        k = (subkey >> (8 * (3 - i))) & 0xFF
        sb = sbox_inv(b, k)
        out = (out << 8) | sb
    return out

# ––– NOVAS FUNÇÕES DE PERMUTAÇÃO –––
def permute(block_int, subkey):
    """
    Permuta os 32 bits do bloco usando um mapeamento linear.
    O mapeamento é:
         nova_pos = (multiplier × i + addend) mod 32
    onde:
         multiplier = (subkey & 0x1F) | 1   (garante que seja ímpar)
         addend = (subkey >> 5) & 0x1F
    Esse mapeamento é invertível.
    """
    multiplier = (subkey & 0x1F) | 1  # Garante valor ímpar
    addend = (subkey >> 5) & 0x1F
    bits = [(block_int >> i) & 1 for i in range(32)]
    permuted = [0] * 32
    for i in range(32):
        new_index = (multiplier * i + addend) % 32
        permuted[new_index] = bits[i]
    out = 0
    for i in range(32):
        out |= (permuted[i] << i)
    return out

def permute_inv(block_int, subkey):
    """
    Inversa da permutação linear.
    Calcula o inverso modular do multiplicador e desfaz o mapeamento:
         original_index = inv_multiplier * (j - addend) mod 32
    """
    multiplier = (subkey & 0x1F) | 1
    addend = (subkey >> 5) & 0x1F
    # Calcula o inverso modular de 'multiplier' modulo 32.
    inv_multiplier = 1
    for x in range(1, 32):
        if (multiplier * x) % 32 == 1:
            inv_multiplier = x
            break
    bits = [(block_int >> i) & 1 for i in range(32)]
    unpermuted = [0] * 32
    for j in range(32):
        original_index = (inv_multiplier * ((j - addend) % 32)) % 32
        unpermuted[original_index] = bits[j]
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

def obter_chave():
    """Função para solicitar e validar a chave informada pelo usuário."""
    while True:
        key_str = input("Chave (8 dígitos hexadecimais, ex.: 1a2b3c4d): ").strip()
        try:
            key = int(key_str, 16)
            if key < 0 or key > 0xFFFFFFFF:
                raise ValueError
            return key
        except ValueError:
            print("Chave inválida! Use 8 dígitos hexadecimais.")

def menu_principal():
    """Exibe o menu interativo e trata as escolhas do usuário."""
    while True:
        print("\n=== INN Seguros - Cifra de Blocos 32 bits ===")
        print("1. Encriptar arquivo")
        print("2. Descriptografar arquivo")
        print("0. Sair")
        opcao = input("Digite a opção desejada: ").strip()
        
        if opcao == "1":
            # Encriptação
            entrada_dir = "Entrada"
            saida_dir = "Criptografado"
            input_file_name = input("Nome do arquivo de entrada (deve ser um .txt na pasta Entrada): ").strip()
            if not input_file_name.lower().endswith('.txt'):
                input_file_name += ".txt"
            input_file = os.path.join(entrada_dir, input_file_name)
            if not os.path.isfile(input_file):
                input_file = criar_arquivo_interativo(entrada_dir, input_file_name)
            output_file_name = input("Nome do arquivo de saída (ex.: saida.txt): ").strip()
            if not output_file_name.lower().endswith('.txt'):
                output_file_name += ".txt"
            os.makedirs(saida_dir, exist_ok=True)
            output_file = os.path.join(saida_dir, output_file_name)
            key = obter_chave()
            process_text_file_encrypt(input_file, output_file, key)
            
        elif opcao == "2":
            # Descriptografia
            entrada_dir = "Criptografado"
            saida_dir = "Descriptografado"
            input_file_name = input("Nome do arquivo de entrada (deve ser um .txt na pasta Criptografado): ").strip()
            if not input_file_name.lower().endswith('.txt'):
                input_file_name += ".txt"
            input_file = os.path.join(entrada_dir, input_file_name)
            if not os.path.isfile(input_file):
                input_file = criar_arquivo_interativo(entrada_dir, input_file_name)
            output_file_name = input("Nome do arquivo de saída (ex.: saida.txt): ").strip()
            if not output_file_name.lower().endswith('.txt'):
                output_file_name += ".txt"
            os.makedirs(saida_dir, exist_ok=True)
            output_file = os.path.join(saida_dir, output_file_name)
            key = obter_chave()
            process_text_file_decrypt(input_file, output_file, key)
            
        elif opcao == "0":
            print("Encerrando...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu_principal()
