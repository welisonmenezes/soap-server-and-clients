import zeep

client = zeep.Client(wsdl='http://127.0.0.1:8888')


def isentryvalid(data):
    try:
        data[2]
    except:
        return False

    if not data[0].isnumeric() or not data[1].isnumeric():
        return False

    valid_operators = ['+', '-', '*', '/', '%']
    if not data[2] in valid_operators:
        return False

    if data[1] == '0' and data[2] == '/':
        print('\nNão é possível dividir por zero')
        return False

    return True


print('-c Calculdora\n-v Validar CPF\n-h Ajuda\n-x Sair\n')

while True:
    user_action = input('Qual operação deseja executar? ')

    if user_action == '-c':
        user_entry = input('Informe os números e o operador, separados por vírgula: ')
        data = user_entry.split(',')

        if not isentryvalid(data):
            print('\nFormato de entrada inválido.\nDigite -h para ajuda.\n')

        else:
            response = client.service.calculadora(float(data[0]), float(data[1]), data[2])
            print('O resultado é: ' + str(response) + '\n')

    elif user_action == '-v':
        user_entry = input('Informe o CPF: ')
        response = client.service.valida_cpf(user_entry)

        if response:
            print('O CPF é válido!\n')

        else:
            print('O CPF é inválido!\n')

    elif user_action == '-h':
        print('\nDigite -c para usar a Calculadora.\n\tModo de usar: Informe os números e o operador, separados por vírgula.\n\t\tExemplo: 9, 9, +\n\t\tOperadores válidos: [+, -, *, /, %]\n\nDigite -v para Validar CPF.\n\tModo de usar: informe o CPF.\n\t\tExemplo: 999.999.999-99 ou 99999999999\n\nDigite -x para sair.\n')
    
    elif user_action == '-x':
        break

    else:
        print('\nOpção inválida. Digite -h para ajuda.\n')