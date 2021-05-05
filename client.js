// npm install soap

const soap = require('soap');
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});

const url = 'http://localhost:8888/';

soap.createClient(url, function(err, client) {
    readline.question(`Escolha um número: `, num => {
        client.verifica_NumeroPar({num: num}, function(err, result) {
            if(err) return console.log(err);
            console.log(result);
        });
        readline.close()
    })
});