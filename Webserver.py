import http.server
import socketserver
import os

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/app.js':
            self.path = '/app.js'
        elif self.path == '/styles.css':
            self.path = '/styles.css'
        elif self.path == '/logo.png':
            self.path = '/logo.png'
        elif self.path == '/data.json':
            self.path = '/data.json'
        super().do_GET()



def run_server():
    web_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    os.chdir(web_dir)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving at port", PORT)
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
