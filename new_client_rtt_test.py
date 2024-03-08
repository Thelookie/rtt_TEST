import socket
import time

SERVER_IP = '54.144.158.134'
SERVER_PORT = 12400

def set_congestion_control_algorithm(sock):
    # TCP 혼잡 제어 알고리즘을 Cubic으로 설정
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'cubic')

def set_receive_window_size(sock, size):
    # 수신 윈도우 크기 설정
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, size)

def get_random_data(sock, size):
    # GET 요청 보내기
    sock.sendall(b'GET /random HTTP/1.1\r\nHost: localhost\r\n\r\n')

    # 응답 받기
    response = b''
    while True:
        # 지정된 윈도우 크기로 데이터 받기
        data = sock.recv(size)
        if not data:
            break
        response += data

    return response

def main():
    try:
        window_size = int(input("수신 윈도우 크기를 입력하세요 (Kbyte): "))
        window_size = window_size*1024
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # 혼잡 제어 알고리즘 설정
            set_congestion_control_algorithm(sock)

            # 수신 윈도우 크기 설정
            set_receive_window_size(sock, window_size)

            # 서버에 연결
            sock.connect((SERVER_IP, SERVER_PORT))

            # 시작 시간 기록
            start_time = time.time()

            # 서버로부터 무작위 데이터 가져오기
            random_data = get_random_data(sock, window_size)

            # 종료 시간 기록
            end_time = time.time()

            # 받은 무작위 데이터 출력
            print("수신한 무작위 데이터:")
            print(random_data.decode('utf-8'))

            # 실행 시간 출력
            elapsed_time = end_time - start_time
            print(f"총 실행 시간: {elapsed_time:.5f} 초")

    except ValueError:
        print("유효한 숫자를 입력하세요.")

if __name__ == "__main__":
    main()
