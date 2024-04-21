import socket
import os
import sys

def set_tcp_congestion_control():
    # Linux에서 TCP 혼잡 제어 알고리즘 설정
    os.system("sysctl -w net.ipv4.tcp_congestion_control=cubic")

def set_initcwnd(sock, initcwnd):
    # initcwnd 설정 (Linux에서만 동작)
    # 이 기능은 root 권한이 필요할 수 있습니다.
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_WINDOW_CLAMP, initcwnd)

def main(initcwnd):
    set_tcp_congestion_control()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8000))
    server_socket.listen(1)
    
    print(f"서버 시작, 포트 12345에서 대기 중, initcwnd={initcwnd}MSS")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"{addr}에서 연결됨")
        
        # initcwnd 설정 적용
        set_initcwnd(client_socket, int(initcwnd) * 1460) # MSS 곱하기
        
        # 클라이언트로부터 데이터 길이 받기
        data_length = client_socket.recv(1024)
        data_length = int(data_length.decode('utf-8'))
        
        # 데이터 길이만큼 랜덤 데이터 생성 및 전송
        random_data = os.urandom(data_length)
        client_socket.sendall(random_data)
        
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <initcwnd in MSS>")
        sys.exit(1)
    main(sys.argv[1])
