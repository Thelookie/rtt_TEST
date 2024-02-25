import socket

SERVER_IP = '166.104.246.42'
SERVER_PORT = 12400
RECV_WINDOW_SIZE = 4  # 수신 윈도우 크기를 조정합니다.

def set_congestion_control_algorithm(sock):
    # TCP 혼잡 제어 알고리즘을 Cubic으로 설정
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'cubic')

def set_receive_window_size(sock, size):
    # 수신 윈도우 크기 설정
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, size)

def get_random_data(sock):
    # GET 요청 보내기
    sock.sendall(b'GET /random HTTP/1.1\r\nHost: localhost\r\n\r\n')

    # 응답 받기
    response = b''
    while True:
        # 지정된 윈도우 크기로 데이터 받기
        data = sock.recv((RECV_WINDOW_SIZE*1024))
        if not data:
            break
        response += data

    return response

# TCP 소켓 생성
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # 혼잡 제어 알고리즘 설정
    set_congestion_control_algorithm(sock)

    # 수신 윈도우 크기 설정
    set_receive_window_size(sock, RECV_WINDOW_SIZE)

    # 서버에 연결
    sock.connect((SERVER_IP, SERVER_PORT))

    # 서버로부터 무작위 데이터 가져오기
    random_data = get_random_data(sock)

# 받은 무작위 데이터 출력
print("수신한 무작위 데이터:")
print(random_data.decode('utf-8'))

