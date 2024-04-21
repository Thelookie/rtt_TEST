import socket
import time

def main(data_length):
    # 결과를 저장할 파일 열기
    with open(f"{data_length}_result.csv", "w") as file:
        file.write("Trial,Time(ms)\n")  # CSV 헤더 작성

        for i in range(30):  # 30번의 요청을 반복
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', 8000))
            
            # 서버에 데이터 길이 요청 전 현재 시간 기록
            start_time = time.time()

            # 서버에 데이터 길이 요청
            client_socket.sendall(str(data_length).encode('utf-8'))
            
            # 서버로부터 랜덤 데이터 수신
            received_data = b''
            while len(received_data) < data_length:
                packet = client_socket.recv(data_length - len(received_data))
                if not packet:
                    break
                received_data += packet

            # 데이터 수신 완료 후 현재 시간 기록
            end_time = time.time()
            
            # 전체 수신 시간 계산 (ms 단위)
            elapsed_time = (end_time - start_time) * 1000
            
            # 결과 파일에 기록
            file.write(f"{i+1},{elapsed_time:.2f}\n")
            
            print(f"시도 {i+1}: 수신 시간 = {elapsed_time:.2f}ms")
            
            client_socket.close()
            time.sleep(1)

if __name__ == "__main__":
    data_length = int(input("요청할 데이터 길이를 입력하세요: "))
    main(data_length)
