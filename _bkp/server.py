#pip install pysimplesoap

from pysimplesoap.server import SoapDispatcher, WSGISOAPHandler
from http.server import BaseHTTPRequestHandler, HTTPServer

# método com a implementação da operação/serviço
def is_par(num):
    print(num)
    return num % 2 == 0

# método com a implementação da operação/serviço
def is_cpf(cpf):
    return True

#criação do objeto soap
dispatcher = SoapDispatcher('AbcBolinhas',
location='http://localhost:8888/',action='http://localhost:8888/',namespace="http://localhost:8888/", prefix="ns0", documentation='Exemplo usando SOAP através de PySimpleSoap', trace=True, debug=True,ns=True)

# publicação do serviço, com seu alias, retorno e parâmetros
dispatcher.register_function('verifica_NumeroPar', is_par, returns={'out0': bool}, args={'num': int})
dispatcher.register_function('verifica_CPF', is_cpf, returns={'out0': bool}, args={'cpf': str})


class SOAPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """User viewable help information and wsdl"""
        args = self.path[1:].split("?")
        if self.path != "/" and args[0] not in self.server.dispatcher.methods.keys():
            self.send_error(404, "Method not found: %s" % args[0])
        else:
            if self.path == "/":
                # return wsdl if no method supplied
                response = self.server.dispatcher.wsdl()
            else:
                # return supplied method help (?request or ?response messages)
                req, res, doc = self.server.dispatcher.help(args[0])
                if len(args) == 1 or args[1] == "request":
                    response = req
                else:
                    response = res

            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.end_headers()
            self.wfile.write(response)

    def do_POST(self):
        """SOAP POST gateway"""
        request = self.rfile.read(int(self.headers.get('content-length')))
        encoding = self.headers.get_param("charset")
        request = request.decode(encoding)
        fault = {}
        # execute the method
        response = self.server.dispatcher.dispatch(request, fault=fault)
        # check if fault dict was completed (faultcode, faultstring, detail)
        if fault:
            self.send_response(500)
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.end_headers()
            self.wfile.write(response)


def main():
    httpd = HTTPServer(("", 8888), SOAPHandler)
    httpd.dispatcher = dispatcher
    httpd.serve_forever()

if __name__ == '__main__':
    main()