import http.server
import socketserver
import random
import threading
import time

SERVER_IP = '192.168.183.128'
PORT = 8000

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()

            # 랜덤 데이터 생성
            random_data = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=1000))
            random_data = random_data.encode('utf-8')

            # 데이터 전송 전 시간 기록
            start_time = time.time()

            # 데이터 전송
            self.wfile.write(random_data)

            # 데이터 전송 후 시간 기록 및 소요 시간 계산
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"데이터를 모두 전송하는 데 걸린 시간: {elapsed_time:.6f} 초")

            # 연결 종료
            self.finish()

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def start_server():
    with socketserver.TCPServer((SERVER_IP, PORT), MyHandler) as httpd:
        print(f"서버가 {SERVER_IP}:{PORT}에서 시작되었습니다.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("사용자가 서버를 종료하였습니다.")

# 서버 실행
server_thread = threading.Thread(target=start_server)
server_thread.start()

