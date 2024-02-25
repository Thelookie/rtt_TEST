import http.server
import socketserver
import random
import string
import socket

SERVER_IP = '192.168.183.130'
PORT = 8000
length = 7000

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/random':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            # 1000-byte length random data
            random_data = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            self.wfile.write(random_data.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def set_congestion_control_algorithm(sock):
    # Set TCP congestion control algorithm to Cubic
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'cubic')

def set_receive_window_size(sock, size):
    # Set receive window size
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, size)

# Create a TCP server
with socketserver.TCPServer((SERVER_IP, PORT), MyHandler) as httpd:
    print(f"Server started at {SERVER_IP}:{PORT}")

    # Set the congestion control algorithm for each incoming connection
    httpd.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    set_congestion_control_algorithm(httpd.socket)
    
    # Set the receive window size for each incoming connection
    set_receive_window_size(httpd.socket, 4096)

    # Serve requests indefinitely
    httpd.serve_forever()

