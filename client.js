const { createClient } = require('soap');
const { resolve } = require('path');
const readline = require('readline');
const rl = readline.createInterface(process.stdin, process.stdout);


function isEntryValid(data) {
    if (data.length < 3) return false;

    if (isNaN(data[0]) || isNaN(data[1])) return false;

    const valid_operators = ['+', '-', '*', '/', '%'];
    if (!valid_operators.includes(data[2])) return false;

    if (data[1] == '0' && data[2] == '/') {
        console.log('\nNão é possível dividir por zero');
        return false;
    }

    return true;
}

console.log('-c Calculdora\n-v Validar CPF\n-h Ajuda\n-x Sair\n');

createClient('http://localhost:8888/', function(err, client) {
    rl.setPrompt('Qual operação deseja executar? ');
    rl.prompt();
    rl.on('line', function(line) {
        switch(line.trim()) {
            case '-c':
                rl.question('Informe os números e o operador, separados por vírgula: ', user_entry => {
                    let data = user_entry.split(',');
                    if (!isEntryValid(data)) {
                        console.log('\nFormato de entrada inválido.\nDigite -h para ajuda.\n');
                        rl.prompt();
                    } else {
                        client.calculadora({num1: data[0], num2: data[1], operador: data[2]}, function(err, result) {
                            console.log('\nO resultado é: ' + result['out0'] + '\n');
                            rl.prompt();
                        });
                    }
                    resolve();
                });
                break;
            case '-v':
                rl.question('Informe o CPF: ', user_entry => {
                    client.valida_cpf({cpf: user_entry}, function(err, result) {
                        if (result['out0']) {
                            console.log('\nO CPF é válido!\n');
                        } else {
                            console.log('\nO CPF é inválido!\n');
                        }
                        rl.prompt();
                    });
                    resolve();
                });
                break;
            case '-h':
                console.log('\nDigite -c para usar a Calculadora.\n\tModo de usar: Informe os números e o operador, separados por vírgula.\n\t\tExemplo: 9, 9, +\n\t\tOperadores válidos: [+, -, *, /, %]\n\nDigite -v para Validar CPF.\n\tModo de usar: informe o CPF.\n\t\tExemplo: 999.999.999-99 ou 99999999999\n\nDigite -x para sair.\n')
                break;
            case '-x':
                rl.close();
            default:
                console.log('\nOpção inválida. Digite -h para ajuda.\n');
            break;
        }
        rl.prompt();
    }).on('close', function() {
        process.exit(0);
    });
});