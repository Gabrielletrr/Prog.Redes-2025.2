import socket

HOST_IP_SERVER = '192.168.0.133'
HOST_PORT      = 50000
CODE_PAGE      = 'utf-8'
BUFFER_SIZE    = 4096
TUPLA_SERVIDOR = (HOST_IP_SERVER, HOST_PORT)

sockClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("\n\nPara sair digite SAIR...\n\n")

while True:

    # Digitar o nome do arquivo
    NomeArquivo = input("Digite o nome do arquivo: ")

    if NomeArquivo.lower().strip() == "sair":
        break

    # Envia o nome do arquivo
    sockClient.sendto(NomeArquivo.encode(CODE_PAGE), TUPLA_SERVIDOR)

    # Recebe confirmação
    ConfirmacaoBytes, TUPLA_SERVIDOR = sockClient.recvfrom(BUFFER_SIZE)
    Confirmacao = ConfirmacaoBytes.decode(CODE_PAGE)

    if Confirmacao == "ERRO":
        print("Arquivo não encontrado.")
        continue

    print("Iniciando download...")

    # Recebendo o tamanho do arquivo
    TamanhoBytes, TUPLA_SERVIDOR = sockClient.recvfrom(BUFFER_SIZE)
    TamanhoArquivo = int(TamanhoBytes.decode(CODE_PAGE))
    print(f"Tamanho total do arquivo: {TamanhoArquivo} bytes")

    # Recebendo o arquivo fragmentado
    conteudo_arquivo = b''
    recebido = 0
    while recebido < TamanhoArquivo:
        parte, TUPLA_SERVIDOR = sockClient.recvfrom(BUFFER_SIZE)
        conteudo_arquivo += parte
        recebido += len(parte)

    print("Download concluído!")

    # Salvando o arquivo
    with open("Recebido_" + NomeArquivo, "wb") as f:
        f.write(conteudo_arquivo)
    print(f"Arquivo salvo como: Recebido_{NomeArquivo}")

sockClient.close()
