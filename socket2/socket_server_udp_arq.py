import socket
from os import path

HOST_IP_SERVER  = ''              # Definindo o IP do servidor
HOST_PORT       = 50000           # Definindo a porta
BUFFER_SIZE     = 1024            # Tamanho do buffer
CODE_PAGE       = 'utf-8'         # Definindo a página de codificação de caracteres

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_DGRAM -> UDP)
sockServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Ligando o socket à porta
sockServer.bind((HOST_IP_SERVER, HOST_PORT))

# Definindo timeout
sockServer.settimeout(0.5)

print('\nRecebendo Mensagens...')
print('Pressione CTRL+C para sair do servidor...\n')
print('-'*100 + '\n')

try:
    while True:
      try:
         
        NomeArquivoBytes, tuplaCliente = sockServer.recvfrom(BUFFER_SIZE)
        NomeArquivo = NomeArquivoBytes.decode(CODE_PAGE).strip()
        print(f'Cliente solicitou: {NomeArquivo}  de  {tuplaCliente}')

        # verifica existência do arquivo
        if not path.exists(NomeArquivo):
            sockServer.sendto('ERRO'.encode(CODE_PAGE), tuplaCliente)
            print('Arquivo não encontrado.')
            continue

        else:
            sockServer.sendto('OK'.encode(CODE_PAGE), tuplaCliente)

        # lê o arquivo inteiro
        with open(NomeArquivo, "rb") as f:
            Conteudo = f.read()
        
        # envia tamanho ao cliente
        TamanhoArquivo = len(Conteudo)
        sockServer.sendto(str(TamanhoArquivo).encode(CODE_PAGE), tuplaCliente)

        i = 0
        while i < TamanhoArquivo:
            parte = Conteudo[i:i+BUFFER_SIZE]
            sockServer.sendto(parte, tuplaCliente)
            i += BUFFER_SIZE
        print('Arquivo enviado com sucesso!')

      except socket.timeout:
         continue
        
        # Enviando a mensagem de volta para o cliente
        
except KeyboardInterrupt:
    print('\nAVISO: Foi Pressionado CTRL+C...\nSaindo do Servidor...\n')

finally:
    sockServer.close()
    print('Servidor finalizado com sucesso...\n')