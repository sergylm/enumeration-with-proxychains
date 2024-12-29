import subprocess
import argparse
from concurrent.futures import ThreadPoolExecutor

def check_open_ports(ip, proxychains_config, top_ports):
    """
    Checks for the most common open ports on a given IP using proxychains and nmap.

    Args:
        ip (str): The target IP address.
        proxychains_config (str): Path to the proxychains configuration file.
        top_ports (int): Number of most common ports to scan.

    Returns:
        list: A list of open ports.
    """
    if top_ports == 0:
        command = ["proxychains", "-f", proxychains_config, "nmap", "-sT", "-p-", "-Pn", "-T4", ip]
    else:
        command = ["proxychains", "-f", proxychains_config, "nmap", "-sT", "--top-ports", str(top_ports), "-Pn", "-T4", ip]

    result = subprocess.run(command, capture_output=True, text=True)

    open_ports = []
    if result.returncode == 0:
        lines = result.stdout.splitlines()
        for line in lines:
            if "/tcp" in line or "/udp" in line:
                parts = line.split()
                if len(parts) >= 2 and "open" in parts[1]:
                    port = parts[0].split('/')[0]
                    open_ports.append(port)
    else:
        print(f"Error scanning {ip} for open ports: {result.stderr}")

    return open_ports

def get_service_info(ip, ports, proxychains_config):
    """
    Gets the service information for a list of open ports on a given IP.

    Args:
        ip (str): The target IP address.
        ports (list): List of open ports.
        proxychains_config (str): Path to the proxychains configuration file.

    Output:
        Prints IP:port service information.
    """
    ports_str = ",".join(ports)
    command = ["proxychains", "-f", proxychains_config, "nmap", "-sV", "-sT", "-p", ports_str, "-Pn", "-T4", ip]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode == 0:
        lines = result.stdout.splitlines()
        for line in lines:
            if "/tcp" in line or "/udp" in line:
                parts = line.split()
                if len(parts) >= 3:
                    port = parts[0].split('/')[0]
                    service = parts[2]
                    print(f"{ip}:{port} {service}")
    else:
        print(f"Error getting service info for {ip}: {result.stderr}")

def process_ip(ip, top_ports, proxychains_config):
    """
    Process an individual IP for open ports and service information.

    Args:
        ip (str): The target IP address.
        top_ports (int): Number of most common ports to scan.
        proxychains_config (str): Path to the proxychains configuration file.
    """
    print(f"Scanning {ip} for the top {top_ports} ports...")
    open_ports = check_open_ports(ip, proxychains_config, top_ports)

    if open_ports:
        print(f"Open ports on {ip}: {', '.join(open_ports)}")
        print(f"Getting service information for {ip}...")
        get_service_info(ip, open_ports, proxychains_config)
    else:
        print(f"No open ports found on {ip}.")

def scan_ports_with_services(ip_list_file, top_ports, proxychains_config="/etc/proxychains.conf", max_threads=5):
    """
    Scans open ports and their services for a list of IPs using proxychains and nmap.

    Args:
        ip_list_file (str): Path to the file containing the list of IPs.
        top_ports (int): Number of most common ports to scan.
        proxychains_config (str): Path to the proxychains configuration file (default: /etc/proxychains.conf).
        max_threads (int): Maximum number of threads to use for parallel processing.

    Output:
        Displays clean IP:port service output in the console.
    """
    try:
        with open(ip_list_file, 'r') as file:
            ip_list = [line.strip() for line in file if line.strip()]

        with ThreadPoolExecutor(max_threads) as executor:
            for ip in ip_list:
                executor.submit(process_ip, ip, top_ports, proxychains_config)

    except FileNotFoundError:
        print(f"File not found: {ip_list_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Script execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan open ports and services using proxychains and nmap.")
    parser.add_argument("ip_list_file", help="Path to the file containing the list of IPs.")
    parser.add_argument("top_ports", type=int, nargs="?", default=10, help="Number of most common ports to scan (default: 10). Use 0 to scan all ports.")
    parser.add_argument("proxychains_config", nargs="?", default="/etc/proxychains.conf", help="Path to the proxychains configuration file (default: /etc/proxychains.conf).")
    parser.add_argument("--threads", type=int, default=5, help="Maximum number of threads to use for parallel processing (default: 5).")

    args = parser.parse_args()

    scan_ports_with_services(args.ip_list_file, args.top_ports, args.proxychains_config, args.threads)
