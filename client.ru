# gem install soap4r-ruby1.9

require 'soap/wsdlDriver'

client = SOAP::WSDLDriverFactory.new( 'http://localhost:8888/' ).create_rpc_driver

puts 'Escolhar um número: '
num = gets.chomp

result = client.verifica_NumeroPar({'num': num});
puts result['out0']