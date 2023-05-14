
from datetime import date,datetime
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from test_covid19.exercise import ReadJsonFile

BASE_URL = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-province.json'

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    # method that responds to GET requests
    def do_GET(self):
        # Specifichiamo il codice di risposta
        self.send_response(200)
        # Specifichiamo uno o più header
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # message that will form the body of the response
        response = requests.get(f"{BASE_URL}")
        data = json.loads(response.text)

        #parameter date
        func = ReadJsonFile()
        parameter_date = func.getPamaterDate()
        if parameter_date:
            print("Selected date: ", parameter_date)
        else:
            return

        # execute code for result
        dict_value = func.getResult(data, parameter_date)
        if dict_value:
            message = "<h1>Lista Casi Totali per Regione nella data : " + parameter_date + "</h1>"
            message = message + "<table border='1px solid black'><tr><td style='font-weight:bold'>Regione</td><td style='font-weight:bold'>Casi</td></tr>"
            for value in dict_value:
                message = message + "<tr><td>" + value[0] + "</td><td>" + str(value[1]) + "</td></tr>"
            message = message + "</table>"
        else:
            message = "No values were found on the selected date: " + parameter_date
        self.wfile.write(message.encode("utf-8"))
        print("Open http://localhost:8000/ to see result.")
        return

    def run():
        print('Avvio del server...')
        # Specifichiamo le impostazioni del server
        # Scegliamo la porta 8081 (per la porta 80 sono necessari i permessi di root)
        server_address = ('localhost', 8000)
        httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
        print('Server in esecuzione...')
        httpd.serve_forever()

testHTTPServer_RequestHandler.run()



