# Importando a biblioteca SOCKET
import socket

# ----------------------------------------------------------------------
HOST_IP_SERVER = '10.25.2.230' # Definindo o IP do servidor
HOST_PORT      = 50000                    # Definindo a porta
CODE_PAGE      = 'utf-8'                  # Definindo a página de 
                                          # codificação de caracteres
BUFFER_SIZE     = 512             # Tamanho do buffer
# ----------------------------------------------------------------------

# Criando o socket (socket.AF_INET -> IPV4 / socket.SOCK_DGRAM -> UDP)
sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print('\n\nPara sair digite SAIR...\n\n')

while True:
   # Informando a mensagem a ser enviada para o servidor
   strMensagem = input('Digite a mensagem: ')

   # Saindo do Cliente quando digitar SAIR
   if strMensagem.lower().strip() == 'sair': break

   # Convertendo a mensagem em bytes
   bytesMensagem = strMensagem.encode(CODE_PAGE) 

   # Enviando a mensagem ao servidor      
   sockUDP.sendto(bytesMensagem, (HOST_IP_SERVER, HOST_PORT))

   # Recebendo a resposta do servidor
   resposta = sockUDP.recvfrom(BUFFER_SIZE)

   print('Resposta enviada pelo servidor: ', resposta.decode(CODE_PAGE))
   print('Resposta recebida com sucesso!')

# Fechando o socket
sockUDP.close()