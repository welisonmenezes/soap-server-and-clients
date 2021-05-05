<?php
$client = new SoapClient("http://localhost:8888/");


function isEntryValid($data) {
    if (!array_key_exists(2, $data)) return false;

    if (!is_numeric($data[0]) || !is_numeric($data[1])) return false;

    $valid_operators = ["+", "-", "*", "/", "%"];
    if (!in_array($data[2], $valid_operators)) return false;

    if ($data[1] == "0" && $data[2] == "/") {
        echo("\nNão é possível dividir por zero\n");
        return false;
    }

    return true;
}


echo("-c Calculdora\n-v Validar CPF\n-h Ajuda\n-x Sair\n\n");

while(true) {
    $user_action = readline("Qual operação deseja executar? ");

    if ($user_action == "-c") {
        $user_entry = readline("Informe os números e o operador, separados por vírgula: ");
        $data = explode(",", $user_entry);
        
        if (!isEntryValid($data)){
            echo("\nFormato de entrada inválido.\nDigite -h para ajuda.\n\n");
        } else {
            $response = $client->calculadora(["num1" => $data[0], "num2" => $data[1], "operador" => $data[2]]);
            echo("O resultado é: " . $response->out0 . "\n\n");
        }

    } else if ($user_action == "-v") {
        $user_entry = readline("Informe o CPF: ");
        $response = $client->valida_cpf(["cpf" => $user_entry]);

        if ($response->out0) {
            echo("O CPF é válido!\n\n");
        } else {
            echo("O CPF é inválido!\n\n");
        }
        
    } else if ($user_action == "-h") {
        echo("\nDigite -c para usar a Calculadora.\n\tModo de usar: Informe os números e o operador, separados por vírgula.\n\t\tExemplo: 9, 9, +\n\t\tOperadores válidos: [+, -, *, /, %]\n\nDigite -v para Validar CPF.\n\tModo de usar: informe o CPF.\n\t\tExemplo: 999.999.999-99 ou 99999999999\n\nDigite -x para sair.\n\n");
    } else if ($user_action == "-x") {
        break;
    } else {
        echo("\nOpção inválida. Digite -h para ajuda.\n");
    }
}
?>