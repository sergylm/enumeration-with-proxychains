# Multi-threaded Port and Service Scanner with Proxychains and Nmap

This script allows you to scan a list of IP addresses for open ports and identify the services running on them. It leverages nmap through proxychains for anonymity and supports multi-threaded scanning for efficiency. It supports:
- Top Ports Scanning: Quickly scan the most common ports or all ports (with -p-) by setting top_ports to 0.
- Service Detection: Identify services running on open ports for a detailed network profile.
- Multithreading: Perform scans in parallel, speeding up the process for large lists of IPs.
- Custom Configuration: Easily configure proxychains and threading through script arguments.

Designed for efficiency and precision, this script is ideal for network engineers, penetration testers, or anyone exploring network security.

# Usage

`python3 script_name.py <ip_list_file> <top_ports> [proxychains_config] [--threads <num_threads>]`

## Arguments
- **ip_list_file**: Path to the file containing IPs to scan (one IP per line).
- **top_ports**: Number of most common ports to scan. Set to 0 to scan all ports.
- **proxychains_config (optional)**: Path to the proxychains configuration file. Defaults to /etc/proxychains.conf.
- **--threads (optional)**: Number of threads for parallel scanning. Defaults to 5.

## Examples
### Example 1: Scan Top 10 Ports with Default Proxychains Config

    python3 enumerate.py ips.txt 10

### Example 2: Scan All Ports (0) with 10 Threads

    python3 enumerate.py ips.txt 0 --threads 10

### Example 3: Use a Custom Proxychains Config

    python3 enumerate.py ips.txt 100 /custom/path/proxychains.conf

### Example 4: Perform a Large Scale Scan with 20 Threads

    python3 enumerate.py large_ips.txt 0 /custom/path/proxychains.conf --threads 20

## Output

The script will display output in the format:
```
Scanning <IP> for the top <N> ports...
Open ports on <IP>: <port1>, <port2>, ...
Getting service information for <IP>...
<IP>:<port1> <service_name>
<IP>:<port2> <service_name>
```

In case of errors or no open ports, appropriate messages will be displayed.


## Requirements

To use this script, ensure the following dependencies are installed on your system:

- Python: Version 3.6 or higher.

        sudo apt-get install python3
  
- Nmap: A network scanning tool.

        sudo apt-get install nmap
  
- Proxychains: For routing traffic through proxies.

        sudo apt-get install proxychains

*Permissions: Sufficient privileges to run network scans (e.g., sudo access if required).*

### Additionally:
- A file containing the list of IPs to scan (one IP per line).
- The default proxychains configuration file is /etc/proxychains.conf. Ensure it is properly set up for your proxy.

### Optional:
- Multi-threading capability can be enhanced by adjusting system limits if scanning many IPs simultaneously.
