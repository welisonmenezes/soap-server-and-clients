use SOAP::Lite +trace;

use strict; use warnings;

my $client = SOAP::Lite->new;
my $ua = $client->schema->useragent;
$ua->agent("Fubar! 0.1");

my $response = $client
    # WSDL url
    ->service("http://localhost:8888/") // the below exposed wsdl

    # method from SOAP server Module
    ->verifica_NumeroPar(1);

print $response;