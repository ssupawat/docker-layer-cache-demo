import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from importlib.metadata import version


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = f"demo app ok\nrich {version('rich')}\nrequests {version('requests')}\n".encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    HTTPServer(("", 8000), Handler).serve_forever()
