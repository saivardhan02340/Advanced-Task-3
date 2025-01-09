import socket
import itertools
import string
import requests
from concurrent.futures import ThreadPoolExecutor

class PenetrationTestingToolkit:
    def __init__(self):
        print("Penetration Testing Toolkit Initialized")

    # Port Scanner
    def port_scanner(self, target, ports, threads=10):
        def scan_port(port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    s.connect((target, port))
                    print(f"[+] Port {port} is open")
            except (socket.timeout, ConnectionRefusedError):
                pass

        with ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(scan_port, ports)

    # Brute-Force Attack (HTTP Basic Auth)
    def brute_force(self, url, username, password_list):
        for password in password_list:
            response = requests.get(url, auth=(username, password))
            if response.status_code == 200:
                print(f"[+] Valid credentials found: {username}:{password}")
                return
        print("[-] No valid credentials found")

    # Subdomain Finder
    def subdomain_finder(self, base_domain, subdomains):
        for sub in subdomains:
            full_url = f"{sub}.{base_domain}"
            try:
                socket.gethostbyname(full_url)
                print(f"[+] Found subdomain: {full_url}")
            except socket.gaierror:
                pass

    # Dictionary Generator
    def dictionary_generator(self, length):
        chars = string.ascii_lowercase + string.digits
        return (''.join(combination) for combination in itertools.product(chars, repeat=length))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Penetration Testing Toolkit")
    parser.add_argument("module", choices=["port_scanner", "brute_force", "subdomain_finder", "dictionary_generator"], help="Select the module to run")

    parser.add_argument("--target", help="Target for the module")
    parser.add_argument("--ports", nargs='+', type=int, help="Ports to scan (for port_scanner)")
    parser.add_argument("--url", help="URL for brute-force or subdomain discovery")
    parser.add_argument("--username", help="Username for brute-force")
    parser.add_argument("--password_list", nargs='+', help="Password list for brute-force")
    parser.add_argument("--subdomains", nargs='+', help="List of subdomains to test")
    parser.add_argument("--length", type=int, help="Length of combinations for dictionary generator")

    args = parser.parse_args()
    toolkit = PenetrationTestingToolkit()

    if args.module == "port_scanner" and args.target and args.ports:
        toolkit.port_scanner(args.target, args.ports)
    elif args.module == "brute_force" and args.url and args.username and args.password_list:
        toolkit.brute_force(args.url, args.username, args.password_list)
    elif args.module == "subdomain_finder" and args.url and args.subdomains:
        toolkit.subdomain_finder(args.url, args.subdomains)
    elif args.module == "dictionary_generator" and args.length:
        for combo in toolkit.dictionary_generator(args.length):
            print(combo)
    else:
        print("[-] Missing or incorrect arguments. Run with -h for help.")
