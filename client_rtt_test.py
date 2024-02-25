import socket
import random
import string

SERVER_IP = '166.104.246.42'
SERVER_PORT = 8000
RECV_WINDOW_SIZE = 4096

def set_congestion_control_algorithm(sock):
    # Set TCP congestion control algorithm to Cubic
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, b'cubic')

def set_receive_window_size(sock, size):
    # Set receive window size
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, size)

def get_random_data(sock):
    # Send GET request
    sock.sendall(b'GET /random HTTP/1.1\r\nHost: localhost\r\n\r\n')

    # Receive response
    response = b''
    while True:
        data = sock.recv(4096)
        if not data:
            break
        response += data

    return response

# Create a TCP socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Set congestion control algorithm
    set_congestion_control_algorithm(sock)

    # Set receive window size
    set_receive_window_size(sock, RECV_WINDOW_SIZE)

    # Connect to the server
    sock.connect((SERVER_IP, SERVER_PORT))

    # Get random data from the server
    random_data = get_random_data(sock)

# Print the received random data
print("Received random data:")
print(random_data.decode('utf-8'))

