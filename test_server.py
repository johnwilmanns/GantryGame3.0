from http.server import BaseHTTPRequestHandler, HTTPServer
import time


hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        code = self.path.lstrip('/').upper()

        try:
            file = open(f"segments_{code}.txt", "r")
            self.wfile.write(bytes(file.read(), "utf-8"))
        except Exception:
            print(f"File not found: segments_{code}.txt")

        


        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        # self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        # self.wfile.write(bytes("<body>", "utf-8"))
        # self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        # self.wfile.write(bytes("</body></html>", "utf-8"))

server = HTTPServer(('localhost', 8080), MyServer)
print ('HTTPServer started')
server.serve_forever()