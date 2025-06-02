import os
from Funcoes.file_utils import (
    process_text_file_encrypt,
    process_text_file_decrypt,
    criar_arquivo_interativo
)

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

def criar_arquivo_menu():
    """Permite ao usuário criar um arquivo .txt na pasta 'Entrada' pelo menu principal."""
    entrada_dir = "Entrada"
    nome_arquivo = input("Digite o nome do novo arquivo (exemplo: meu_arquivo.txt): ").strip()
    if not nome_arquivo.lower().endswith('.txt'):
        nome_arquivo += ".txt"
    caminho = os.path.join(entrada_dir, nome_arquivo)
    if os.path.isfile(caminho):
        print(f"O arquivo '{caminho}' já existe.")
        return
    conteudo = input("Digite o conteúdo do arquivo (em uma linha ou cole o texto desejado):\n")
    os.makedirs(entrada_dir, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"Arquivo '{caminho}' criado com sucesso!")

def menu_principal():
    """Exibe o menu interativo e trata as escolhas do usuário."""
    while True:
        print("\n=== INN Seguros - Cifra de Blocos 32 bits ===")
        print("1. Encriptar arquivo")
        print("2. Descriptografar arquivo")
        print("3. Criar novo arquivo .txt na pasta Entrada")
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
        
        elif opcao == "3":
            # Criar novo arquivo .txt na pasta Entrada
            criar_arquivo_menu()
        
        elif opcao == "0":
            print("Encerrando...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")