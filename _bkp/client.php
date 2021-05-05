<?php 
// extension=soap

$option=array('trace'=>1); 
$client = new SoapClient("http://localhost:8888/", $option);
$num = readline("Escolha um número: ");
$response = $client->verifica_NumeroPar([ 'num' => $num ]);
print_r($response);
?>