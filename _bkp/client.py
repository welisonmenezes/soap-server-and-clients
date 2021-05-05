#pip install zeep

import zeep

client = zeep.Client(wsdl='http://127.0.0.1:8888')

num = input('Escolha um número: ')
print( client.service.verifica_NumeroPar(num) )