import socket
import signal
import sys
import ipaddress
import argparse
from concurrent.futures import ThreadPoolExecutor

print("""
                          888                                                                       
                          888                                                                       
                          888                                                                       
88888b.   .d88b.  888d888 888888      .d8888b   .d8888b  8888b.  88888b.  88888b.   .d88b.  888d888 
888 "88b d88""88b 888P"   888         88K      d88P"        "88b 888 "88b 888 "88b d8P  Y8b 888P"   
888  888 888  888 888     888         "Y8888b. 888      .d888888 888  888 888  888 88888888 888     
888 d88P Y88..88P 888     Y88b.            X88 Y88b.    888  888 888  888 888  888 Y8b.     888     
88888P"   "Y88P"  888      "Y888       88888P'  "Y8888P "Y888888 888  888 888  888  "Y8888  888     
888                                                                                                 
888                                                                                                
888
                                          latews                 
      """)

def scan_target(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((ip, port))
            print(f"[+] {ip} -> {port} - Open")
    except (socket.timeout, socket.error):
        pass

def scan(ip, ports, max_threads=10):
    print(f"Scanning {ip}...")
    with ThreadPoolExecutor(max_threads) as executor:
        for port in ports:
            executor.submit(scan_target, ip, port)
def parse_port_range(port_range):
    try:
        start, end = map(int, port_range.split('-'))
        if start > end or start < 1 or end > 65535:
            raise argparse.ArgumentTypeError("Invalid port range")
        return range(start, end + 1)
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid port range")

def args():
    parser = argparse.ArgumentParser(description='Simple port scanner')
    parser.add_argument('-i', '--ip', help='Target IP address', required=True)
    parser.add_argument('-p', '--port', type=parse_port_range, help='Target port range (e.g., 100-277)', required=True)

    args = parser.parse_args()
    scan(args.ip, args.port)
if __name__ == "__main__":
    args()


