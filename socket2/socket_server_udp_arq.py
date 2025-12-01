import socket
from os import path

HOST_IP_SERVER  = ''          
HOST_PORT       = 50000
BUFFER_SIZE     = 4096
CODE_PAGE       = 'utf-8'

sockServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sockServer.bind((HOST_IP_SERVER, HOST_PORT))

print('\nServidor aguardando arquivos...\n')

try:
    while True:
       
        # Recebendo nome do arquivo 
        NomeArquivoBytes, tuplaCliente = sockServer.recvfrom(BUFFER_SIZE)
        NomeArquivo = NomeArquivoBytes.decode(CODE_PAGE).strip()
        print(f'Cliente solicitou: {NomeArquivo} de {tuplaCliente}')

        # Conferir se o arquivo existe 
        if not path.exists(NomeArquivo):
            sockServer.sendto('ERRO'.encode(CODE_PAGE), tuplaCliente)
            continue

        sockServer.sendto('OK'.encode(CODE_PAGE), tuplaCliente)

        # Abrir e ler o arquivo
        with open(NomeArquivo, "rb") as f:
            Conteudo = f.read()

        # Verificar o tamanho do arquivo e envia
        TamanhoArquivo = len(Conteudo)
        sockServer.sendto(str(TamanhoArquivo).encode(CODE_PAGE), tuplaCliente)

        # Envia o arquivo fragmentado
        i = 0
        while i < TamanhoArquivo:
            parte = Conteudo[i:i+BUFFER_SIZE]
            sockServer.sendto(parte, tuplaCliente)
            i += BUFFER_SIZE
        print("Arquivo enviado com sucesso!")

except KeyboardInterrupt:
    print("\nSaindo...")

finally:
    sockServer.close()
