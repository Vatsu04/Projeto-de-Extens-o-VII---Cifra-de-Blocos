input = input("Digite o nome do arquivo em binario a ser lido:")



with open(f"criptografado/{input}", "rb") as f:
    data = f.read()
    print(repr(data))