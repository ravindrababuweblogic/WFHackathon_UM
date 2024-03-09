import http.server
import socketserver

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello, World!')

with socketserver.TCPServer(("", 8000), SimpleHTTPRequestHandler) as httpd:
    print("serving at port", httpd.server_address[1])
    httpd.serve_forever()