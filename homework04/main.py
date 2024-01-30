import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from datetime import datetime
import json
import threading
import socket


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('./index.html')
        elif pr_url.path == '/massage':
            self.send_html_file('./massage.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('./error.html', 404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        content_type = self.headers['Content-Type']

        data = self.rfile.read(content_length)

        if 'application/x-www-form-urlencoded' in content_type:
            data_parse = {key: value[0] for key, value in urllib.parse.parse_qs(data.decode()).items()}
            print(data_parse)
            self.save_to_socket_file(data_parse)
        else:
            print(f"Unsupported Content-Type: {content_type}")

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt, _ = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt)
        else:
            self.send_header("Content-type", 'application/octet-stream')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def save_to_socket_file(self, data):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_dict = {
            "username": data['username'][0],
            "message": data['message'][0]
        }

        with open('./storage/data.json', 'a') as json_file:
            json.dump(data_dict, json_file, indent=4)
            json_file.write('\n')


def run():
    http_server_thread = threading.Thread(target=lambda: HTTPServer(('localhost', 3000), HttpHandler).serve_forever())
    http_server_thread.start()

    socket_server_thread = threading.Thread(target=socket_server)
    socket_server_thread.start()

    http_server_thread.join()
    socket_server_thread.join()


def socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('localhost', 5000))
        print('Socket server listening on localhost:5000')

        while True:
            data, addr = s.recvfrom(1024)
            print(f'Received data from {addr}: {data.decode()}')


if __name__ == '__main__':
    run()
