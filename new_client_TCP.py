import socket
import time
import csv

SERVER_IP = '54.144.158.134'
SERVER_PORT = 8000
def set_congestion_control_algorithm(sock):
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'cubic')

def set_receive_window_size(sock, size):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, size)

def get_random_data(sock, size):
    sock.sendall(b'GET /random HTTP/1.1\r\nHost: localhost\r\n\r\n')
    response = b''
    while True:
        data = sock.recv(size)
        if not data:
            break
        response += data
    return response

def run_test(window_size):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        set_congestion_control_algorithm(sock)
        set_receive_window_size(sock, window_size)
        sock.connect((SERVER_IP, SERVER_PORT))
        start_time = time.time()
        _ = get_random_data(sock, window_size)
        end_time = time.time()
        return end_time - start_time

def main():
    window_sizes_kb = [4, 16, 64, 128, 1024]
    iterations = 30
    results = {size: [] for size in window_sizes_kb}
    start = input("please press enter key...")

    for size in window_sizes_kb:
        print(f"Testing with window size: {size}K")
        for _ in range(iterations):
            elapsed_time = run_test(size * 1024)
            time.sleep(1)
            results[size].append(elapsed_time)
            print(f"Elapsed time: {elapsed_time:.5f} seconds")

    for size in window_sizes_kb:
        results[size].sort()

    with open('tcp_test_results.csv', 'w', newline='') as csvfile:
        fieldnames = [f"{size}K" for size in window_sizes_kb]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for _ in range(iterations):
            row = {f"{size}K": results[size][_] for size in window_sizes_kb}
            writer.writerow(row)

if __name__ == "__main__":
    main()
