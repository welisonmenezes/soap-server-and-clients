require "soap/wsdlDriver"

client = SOAP::WSDLDriverFactory.new( "http://localhost:8888/" ).create_rpc_driver


class String
    def numeric?
      Float(self) != nil rescue false
    end
end


def isEntryValid(data)
    if (data.length() < 3) 
        return false 
    end

    if (!data[0].numeric? || !data[1].numeric?)
        return false
    end

    valid_operators = ["+", "-", "*", "/", "%"]
    if (!valid_operators.include? data[2])
        return false
    end

    if (data[1] == "0" && data[2] == "/")
        puts "\nNão é possível dividir por zero\n"
        return false
    end

    return true
end


puts "-c Calculdora\n-v Validar CPF\n-h Ajuda\n-x Sair\n\n"

while true
    puts "Qual operação deseja executar? "
    user_action = gets.chomp
    
    if user_action == "-c"
        puts "\nInforme os números e o operador, separados por vírgula: "
        user_entry = gets.chomp
        data = user_entry.split(",", -1)

        if (!isEntryValid(data))
            puts "\nFormato de entrada inválido.\nDigite -h para ajuda.\n\n"
        else
            result = client.calculadora({"num1": data[0], "num2": data[1], "operador": data[2]});
            puts "\nO resultado é: " + result["out0"] + "\n\n"
        end

    elsif user_action == "-v"
        puts "\nInforme o CPF: "
        user_entry = gets.chomp
        result = client.valida_cpf({"cpf": user_entry});
        
        if (result["out0"] == "true")
            puts "\nO CPF é válido!\n\n"
        else
            puts "\nO CPF é inválido!\n\n"
        end

    elsif user_action == "-h"
        puts "\nDigite -c para usar a Calculadora.\n\tModo de usar: Informe os números e o operador, separados por vírgula.\n\t\tExemplo: 9, 9, +\n\t\tOperadores válidos: [+, -, *, /, %]\n\nDigite -v para Validar CPF.\n\tModo de usar: informe o CPF.\n\t\tExemplo: 999.999.999-99 ou 99999999999\n\nDigite -x para sair.\n\n"
    elsif user_action == "-x"
        break
    else
        puts "\nOpção inválida. Digite -h para ajuda.\n\n"
    end
end