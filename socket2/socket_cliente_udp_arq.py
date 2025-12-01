# Importando a biblioteca SOCKET
import socket

HOST_IP_SERVER = '192.168.0.5'                # Definindo o IP do servidor
HOST_PORT      = 50000                        # Definindo a porta
CODE_PAGE      = 'utf-8'                      # Definindo a página de codificação de caracteres
BUFFER_SIZE    = 1024                         # Tamanho do buffer
TUPLA_SERVIDOR = HOST_IP_SERVER, HOST_PORT

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_DGRAM -> UDP)
sockClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('\n\nPara sair digite SAIR...\n\n')

while True:
  # Informando a mensagem a ser enviada para o servidor
  strMensagem = input('Digite a mensagem: ')

  # Saindo do Cliente quando digitar SAIR
  if strMensagem.lower().strip() == 'sair': break

  # Enviando tamanho da mensagem
  dados = strMensagem.encode(CODE_PAGE)
  TamanhoMensagem = len(dados)
  sockClient.sendto(str(TamanhoMensagem).encode(CODE_PAGE), TUPLA_SERVIDOR)
  print('Tamanho da mensagem', TamanhoMensagem)

  
  # Enviando a mensagem fragmentada
  i = 0
  while i < TamanhoMensagem:
    fragmento = strMensagem[i:i+BUFFER_SIZE]
    sockClient.sendto((str(fragmento).encode(CODE_PAGE)), TUPLA_SERVIDOR)
    i += BUFFER_SIZE  

  # Recebendo resposta do servidor 
  Resposta = ''
  Partes = 0
  while Partes < TamanhoMensagem:
    bytesMensagem, end_server = sockClient.recvfrom(BUFFER_SIZE)
    MensagemResposta = bytesMensagem.decode(CODE_PAGE)
    Resposta += MensagemResposta
    Partes += len(MensagemResposta)
  print(f'Resposta Servidor: {Resposta}')

# Fechando o socket
sockClient.close()