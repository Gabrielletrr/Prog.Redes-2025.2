import socket

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
            
         # Recebendo o tamanho da mensagem
         TamanhoMensagemBytes, tuplaCliente = sockServer.recvfrom(BUFFER_SIZE)
         intTamanhoMensagens = int(TamanhoMensagemBytes.decode(CODE_PAGE))
         print(f"Tamanho informado pelo cliente: {intTamanhoMensagens} bytes")

         # Recebendo fragmentos da mensagem
         Mensagem = ''
         Fragmentos = 0
        
         while Fragmentos < intTamanhoMensagens:
            MensagemBytes, tuplaCliente = sockServer.recvfrom(BUFFER_SIZE)
            strMensagem = MensagemBytes.decode(CODE_PAGE)
            Mensagem += strMensagem
            Fragmentos += len(strMensagem)
         print(f'Mensagem completa: {Mensagem}')
         
      except socket.timeout:
         continue
        
      else:
         try:
            # Obtendo o nome (HOST) do cliente
            strNomeHost = socket.gethostbyaddr(tuplaCliente[0])[0]
            strNomeHost = strNomeHost.split('.')[0].upper()
         except socket.herror:
            strNomeHost = tuplaCliente[0]

         print(f'{tuplaCliente} -> {strNomeHost}: {Mensagem}')

         # Enviando a mensagem de volta para o cliente
         i = 0
         while i < intTamanhoMensagens:
            parte = Mensagem[i:i+BUFFER_SIZE]
            sockServer.sendto(str(parte).encode(CODE_PAGE), tuplaCliente)
            i += BUFFER_SIZE
      
except KeyboardInterrupt:
    print('\nAVISO: Foi Pressionado CTRL+C...\nSaindo do Servidor...\n')

finally:
    sockServer.close()
    print('Servidor finalizado com sucesso...\n')
