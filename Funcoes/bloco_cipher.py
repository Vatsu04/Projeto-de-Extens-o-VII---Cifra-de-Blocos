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
    print(f"  [Encrypt] Bloco inicial: {block_bytes.hex()} ({block:08x})")
    for i in range(3):
        block_pre_sub = block
        block = substitute(block, subkeys[i])
        print(f"    [Rodada {i+1}] Após substitute: {block:08x}")
        block = permute(block, subkeys[i])
        print(f"    [Rodada {i+1}] Após permute   : {block:08x} (subkey: {subkeys[i]:08x})")
    print(f"  [Encrypt] Bloco final  : {block:08x}\n")
    return block.to_bytes(4, "big")

def decrypt_block(block_bytes, subkeys):
    block = int.from_bytes(block_bytes, "big")
    print(f"  [Decrypt] Bloco inicial: {block_bytes.hex()} ({block:08x})")
    for idx, i in enumerate(reversed(range(3))):
        block_pre_perm = block
        block = permute_inv(block, subkeys[i])
        print(f"    [Rodada {3-idx}] Após permute_inv: {block:08x}")
        block = substitute_inv(block, subkeys[i])
        print(f"    [Rodada {3-idx}] Após substitute_inv: {block:08x} (subkey: {subkeys[i]:08x})")
    print(f"  [Decrypt] Bloco final  : {block:08x}\n")
    return block.to_bytes(4, "big")