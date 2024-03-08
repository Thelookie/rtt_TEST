import subprocess
import socket
import time
import csv

SERVER_IP = '54.144.158.134'
SERVER_PORT = 12400
network_interface = "wlo1"

def set_packet_loss(loss_rate):
    subprocess.run(["sudo", "tc", "qdisc", "del", "dev", network_interface, "root"], stderr=subprocess.DEVNULL)
    subprocess.run(["sudo", "tc", "qdisc", "add", "dev", network_interface, "root", "netem", "loss", f"{loss_rate}%"])

def reset_network():
    subprocess.run(["sudo", "tc", "qdisc", "del", "dev", network_interface, "root"], stderr=subprocess.DEVNULL)

def set_congestion_control_algorithm(sock):
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'cubic')

def set_receive_window_size(sock, size):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, size)

def get_random_data(sock, size):
    sock.sendall(b'GET /random HTTP/1.1\r\nHost: localhost\r\n\r\n')
    start_time = time.time()
    response = b''
    while True:
        data = sock.recv(size)
        if not data:
            break
        response += data
    end_time = time.time()
    return response, start_time, end_time

def run_test(window_size):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        set_congestion_control_algorithm(sock)
        set_receive_window_size(sock, window_size)
        sock.connect((SERVER_IP, SERVER_PORT))
        _, start_time, end_time = get_random_data(sock, window_size)
        elapsed_time = end_time - start_time
    return elapsed_time

def main():
    results = [["Loss Rate (%)", "Iteration", "Execution Time (s)"]]
    try:
        window_size = int(input("수신 윈도우 크기를 입력하세요 (Kbyte): ")) * 1024
    except ValueError:
        print("유효한 숫자를 입력하세요.")
        return  # 종료
   
    for loss_rate in range(5, 25, 5):
        for iteration in range(1, 31):
            print(f"패킷 손실율: {loss_rate}%, 반복: {iteration}")
            set_packet_loss(loss_rate)
            execution_time = run_test(window_size)
            results.append([loss_rate, iteration, execution_time])
            time.sleep(0.5)

    reset_network()
    print("네트워크 설정이 초기화되었습니다.")

    with open("result.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(results)
    print("결과가 result.csv 파일에 저장되었습니다.")

if __name__ == "__main__":
    main()

    
