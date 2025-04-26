
 

# Desenvolvimento de um Algoritmo de Cifra de Blocos 

 





A Inn Seguros, uma renomada seguradora, identificou a necessidade de desenvolver um sistema próprio de criptografia para armazenar seus registros com maior segurança. Preocupada com possíveis violações de dados e vazamentos, a empresa contratou sua equipe de especialistas em segurança da informação para projetar e implementar um algoritmo de cifra de blocos simétrica, capaz de proteger informações críticas de clientes, como contratos, sinistros e dados pessoais. 



O objetivo deste trabalho é criar um algoritmo de criptografia que atenda aos requisitos da Inn Seguros, garantindo confidencialidade, integridade e eficiência no processamento de dados. O algoritmo deve ser implementado em código, sem o uso de bibliotecas externas de criptografia, e acompanhado de um documento técnico detalhando suas operações. 



# Requisitos do Algoritmo 



O algoritmo deve seguir as seguintes especificações: 

Tipo de Cifra: Cifra de blocos simétrica. 
Tamanho do bloco: 32 bits. 
Tamanho da chave: 32 bits. 
Rodadas de processamento: 3 rodadas, cada uma com operações de substituição e permutação dependentes da chave. 
Derivação de chaves: Cada rodada deve usar uma subchave derivada da chave principal. 
Efeito avalanche: Pequenas mudanças no texto claro ou na chave devem gerar grandes alterações no texto cifrado. 
Além disso, o programa deve: 

Ser capaz de encriptar e decriptar arquivos. 
Ser auto-suficiente, sem dependências externas. 
Ter código fonte comentado, especialmente nas funções de criptografia. 
O algoritmo deve executar, pelo menos, as seguintes operações em cada rodada: 

Geração de subchaves para cada rodada, derivadas da chave principal. 
Aplicação de substituição, dependente da chave. 
Aplicação de permutação, dependente da chave. 
 

# Implementação do Programa 



O programa deve: 

Ler um arquivo de entrada e processá-lo em blocos de 32 bits. 
Permitir a escolha entre encriptar e decriptar. 
Gerar um arquivo de saída com o resultado. 
Ser desenvolvido em linguagem de programação à escolha do grupo (C, Python, Java, etc.), sem bibliotecas externas de criptografia. 
 

# Documentação Técnica 



O documento deve seguir as normas ABNT para o desenvolvimento de trabalhos acadêmicos e deve conter: 

Capa com nome completo dos integrantes. 
Introdução e justificativa. 
Descrição detalhada do algoritmo (cifra de substituição, cifra de permutação, derivação de chaves, etc.). 
Explicação do efeito avalanche. 
Exemplo de texto cifrado com o resultado parcial de cada rodada. Fazer dois exemplos encriptados com chaves que diferem em apenas 1 bit para verificar o efeito avalanche. 
Referências bibliográficas. 
 

# Critérios de Avaliação 



O trabalho será avaliado com base em: 

Correta implementação do algoritmo. 
Funcionamento do programa (encriptação e decriptação). 
Qualidade da documentação técnica. 
Originalidade e complexidade das operações. 
Efeito avalanche e difusão eficientes. 
 

# Entrega 



A entrega deverá ser realizada pela equipe Teams montada para o desenvolvimento deste projeto de extensão, na área de entrega de trabalhos. 



Prazo de entrega: 13/06/2025. 



Formato de entrega: Código fonte comentado e documento em formato PDF.   

 

# Considerações Finais 



O trabalho pode ser entregue em grupos de até 5 alunos. 



A entrega deve ser exclusivamente por intermédio de envio de trabalhos da equipe Teams. Qualquer tentativa de entrega por outros meios será desconsiderada. 

O programa pode ser desenvolvido em linguagem de programação à escolha do grupo, porém não podem ser utilizadas facilidades de criptografia nem da linguagem nem de bibliotecas externas. 



O programa não pode ter dependências externas para sua compilação ou execução. Se for desenvolvido em linguagem de programação compilada sua compilação deve poder ser realizada no compilador padrão da linguagem, sem dependência de frameworks. Se for uma linguagem interpretada, sua execução deve ocorrer no interpretador padrão da linguagem, sem nenhum tipo de necessidade de importação de bibliotecas externas nem de execução em frameworks específicos. 



O código fonte deve estar comentado, em particular as partes que implementam as funções de encriptação e decriptação.
