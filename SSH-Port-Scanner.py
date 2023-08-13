import threading
import random
import time
import socket
from ping3 import ping

# Function to ping an IP address
def ping_ip(ip):
    try:
        result = ping(ip)
        if result is not None:
            return ip
    except:
        pass

# Function to generate random IP addresses
def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

# Function to check if a port is open
def check_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Adjust the timeout as needed
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            return True
        else:
            return False

    except socket.error:
        return False

# Function to perform pinging and port scanning with threading
def ping_and_scan_with_threads(num_threads):
    while True:
        ips = [generate_random_ip() for _ in range(10)]
        threads = []

        for ip in ips:
            thread = threading.Thread(target=ping_and_scan, args=(ip,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        time.sleep(5)  # Wait for 5 seconds before generating new IPs

# Function to ping an IP, collect online IPs with open port 22
def ping_and_scan(ip):
    result = ping_ip(ip)
    if result and check_port(result, 22):
        print(f"IP: {result}, Port 22 is open")
        with open("port_22_results.txt", "a") as outfile:
            outfile.write(f"{result}:22\n")
    
if __name__ == "__main__":
    num_threads = 50
    thread_list = []

    for _ in range(num_threads):
        thread = threading.Thread(target=ping_and_scan_with_threads, args=(num_threads,))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()
