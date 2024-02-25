import http.server
import socketserver
import random
import string
import socket
import subprocess

SERVER_IP = '192.168.183.130'
PORT = 12400
length = 4096

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/random':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            # 1000바이트 길이의 랜덤 데이터 생성
            random_data = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            self.wfile.write(random_data.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def set_congestion_control_algorithm():
    subprocess.run(["sysctl", "-w", "net.ipv4.tcp_congestion_control=cubic"])

with socketserver.TCPServer((SERVER_IP, PORT), MyHandler) as httpd:
    print(f"서버가 {SERVER_IP}:{PORT}에서 시작되었습니다.")

    # Set the congestion control algorithm to Cubic
    set_congestion_control_algorithm()

    httpd.serve_forever()
