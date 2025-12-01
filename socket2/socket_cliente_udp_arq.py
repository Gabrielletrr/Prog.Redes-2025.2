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
  NomeArquivo = input('Digite o nome do arquivo: ')

  # Saindo do Cliente quando digitar SAIR
  if NomeArquivo.lower().strip() == 'sair': break

  # Envia o nome do arquivo para o servidor
  sockClient.sendto(NomeArquivo.encode(CODE_PAGE), TUPLA_SERVIDOR)

  # Recebendo a confirmação
  ConfirmacaoBytes, TUPLA_SERVIDOR = sockClient.recvfrom(BUFFER_SIZE)
  Confirmacao = ConfirmacaoBytes.decode(CODE_PAGE)

  if ConfirmacaoBytes == 'ERRO':
    print('Arquivo não encontrado')
  else:
    print('Iniciando download ...')

    # Recebendo o tamanho do arquivo
    TamanhoBytes, TUPLA_SERVIDOR = sockClient.recvfrom(BUFFER_SIZE)
    TamanhoArquivo = int(TamanhoBytes.decode(CODE_PAGE)) 
    print(f'Tamanho total do arquivo {TamanhoArquivo}')

    # Recebendo resposta do servidor 
    Resposta = ''
    Partes = 0
    while Partes < TamanhoArquivo:
      bytesMensagem, end_server = sockClient.recvfrom(BUFFER_SIZE)
      Resposta += bytesMensagem
      Partes += len(Resposta)
    print(f'Resposta Servidor: {Resposta}')

    # Salvando o arquivo
    with open('Recebido_' + NomeArquivo, 'wb') as f:
      f.write(Resposta)

# Fechando o socket
sockClient.close()