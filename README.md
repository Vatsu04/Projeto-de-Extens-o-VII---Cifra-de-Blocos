# INN Seguros - Cifra de Blocos 32 bits

Este projeto implementa uma cifra de bloco de 32 bits para criptografia e descriptografia de arquivos texto. Ele foi desenvolvido como uma solução didática para demonstrar conceitos de cifragem por blocos, manipulação de arquivos em Python e separação modular de código.

## Estrutura dos Arquivos

O projeto está organizado da seguinte forma:

```
├── main.py
└── Funcoes/
    ├── bloco_cipher.py
    ├── file_utils.py
    └── user_interface.py
```

- **main.py**: Ponto de entrada do programa. Executa o menu interativo.
- **Funcoes/bloco_cipher.py**: Funções relacionadas à cifra de bloco, subchaves, substituição, permutação e operações de cifra/decifra.
- **Funcoes/file_utils.py**: Funções para manipulação de arquivos texto, incluindo leitura, escrita, criação interativa e processamento de criptografia/descriptografia.
- **Funcoes/user_interface.py**: Funções de interação com o usuário, como o menu principal e obtenção da chave.

## Como usar

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/seu-repo.git
   cd seu-repo
   ```

2. **Certifique-se que a estrutura de pastas está conforme acima.**

3. **Execute o programa principal:**

   ```bash
   python main.py
   ```

4. **Siga as instruções do menu interativo:**
   - Para encriptar ou descriptografar, insira os nomes dos arquivos e a chave de 8 dígitos hexadecimais quando solicitado.

## Funcionamento

- Os arquivos de entrada para **encriptação** devem estar na pasta `Entrada/`.
- Os arquivos criptografados serão salvos em `Criptografado/`.
- Os arquivos descriptografados serão salvos em `Descriptografado/`.
- Caso algum arquivo de entrada não exista, o programa permite a sua criação interativa.

## Sobre a cifra

- Utiliza blocos de 32 bits (4 bytes).
- A chave deve ser fornecida como um número hexadecimal de 8 dígitos (exemplo: `1a2b3c4d`).
- O algoritmo deriva 3 subchaves da chave principal e aplica rodadas de substituição e permutação.
- O último bloco do arquivo recebe padding, se necessário.

## Requisitos

- Python 3.7 ou superior.

## Observações

- O sistema foi desenvolvido para fins didáticos e não deve ser utilizado como solução de segurança para dados sensíveis em produção.
- Recomenda-se executar sempre em ambiente seguro e controlado.

- ## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

