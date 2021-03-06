from pysimplesoap.server import SoapDispatcher, WSGISOAPHandler
from http.server import BaseHTTPRequestHandler, HTTPServer
import re


def calculadora(num1, num2, operador):
    if operador == '+':
        return num1 + num2

    if operador == '-':
        return num1 - num2

    if operador == '/':
        return num1 / num2

    if operador == '*':
        return num1 * num2

    if operador == '%':
        return num1 % num2

    return 0


def valida_cpf(cpf):
    cpf = ''.join(re.findall(r'\d', str(cpf)))

    if not cpf or len(cpf) < 11:
        return False

    antigo = [int(d) for d in cpf]
    novo = antigo[:9]

    while len(novo) < 11:
        resto = sum([v * (len(novo) + 1 - i) for i, v in enumerate(novo)]) % 11
        digito_verificador = 0 if resto <= 1 else 11 - resto
        novo.append(digito_verificador)

    if novo == antigo:
        return True

    return False


dispatcher = SoapDispatcher('AbcBolinhas',
location='http://localhost:8888/',action='http://localhost:8888/',namespace="http://localhost:8888/", prefix="ns0", documentation='Exemplo usando SOAP através de PySimpleSoap', trace=True, debug=True,ns=True)
dispatcher.register_function('calculadora', calculadora, returns={'out0': float}, args={'num1': float, 'num2': float, 'operador': str})
dispatcher.register_function('valida_cpf', valida_cpf, returns={'out0': bool}, args={'cpf': str})


class SOAPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        args = self.path[1:].split("?")

        if self.path != "/" and args[0] not in self.server.dispatcher.methods.keys():
            self.send_error(404, "Method not found: %s" % args[0])

        else:
            if self.path == "/":
                response = self.server.dispatcher.wsdl()

            else:
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
        request = self.rfile.read(int(self.headers.get('content-length')))
        encoding = self.headers.get_param("charset")
        request = request.decode(encoding)
        fault = {}
        response = self.server.dispatcher.dispatch(request, fault=fault)

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