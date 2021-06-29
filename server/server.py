from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver

port = 8080
hostname = 'localhost'

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open('index.html', 'rb') as f:
            self.wfile.write(f.read())

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = (hostname, port)
    httpd = server_class(server_address, handler_class)
    print("Server started http://%s:%s" % (hostname, port))

    httpd.serve_forever()



if __name__=='__main__':
    run(handler_class=RequestHandler)