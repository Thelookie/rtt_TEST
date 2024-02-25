import requests
import subprocess

server_ip = '192.168.183.130'
port = 12400
receive_window_size = 4096  # Set receive window size to 4 KB

def set_congestion_control_algorithm():
    subprocess.run(["sysctl", "-w", "net.ipv4.tcp_congestion_control=cubic"])

def set_receive_window_size():
    global receive_window_size
    subprocess.run(["sysctl", "-w", f"net.ipv4.tcp_rmem='{receive_window_size} {receive_window_size} {receive_window_size}'"])

def main():
    # Set the congestion control algorithm to Cubic
    set_congestion_control_algorithm()

    # Set the receive window size
    set_receive_window_size()

    url = f'http://{server_ip}:{port}/random'
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Received random data:")
        print(response.text)
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    main()
