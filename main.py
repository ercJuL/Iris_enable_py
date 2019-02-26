from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer


class MyHttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve a GET request."""
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        self.wfile.write(b'SUCCESS')  # 此处修改返回标识




if __name__ == '__main__':
    http_server = HTTPServer(('', int(80)), MyHttpServer)
    http_server.serve_forever()
