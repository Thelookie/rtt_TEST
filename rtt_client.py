import socket
import time

SERVER_IP = '166.104.246.42'
PORT = 8000

def send_request():
    while True:
        # 서버에 접속하여 데이터 요청
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, PORT))

            # 데이터 수신 전 시간 기록
            start_time = time.time()

            response = s.recv(1024)
            print(f"받은 데이터: {response.decode('utf-8')}")

            # 데이터 수신 후 시간 기록 및 소요 시간 계산
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"데이터를 모두 수신하는 데 걸린 시간: {elapsed_time:.6f} 초")

            time.sleep(1)

# 클라이언트 실행
send_request()

