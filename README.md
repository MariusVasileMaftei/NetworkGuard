# NetworkGuard

A lightweight Python tool for automated network reconnaissance and local system auditing. Built for security researchers to capture environment snapshots during target scans.

## Features
- **Host Audit**: Logs local interface states (IP, MAC, Network) before remote scans.
- **Remote Recon**: Automates connectivity checks and path tracing to a target IP.
- **Log Management**: Automatically organizes results into timestamped directories.
- **Data Parsing**: Uses Regex to extract structured network data from raw `ip addr` output.

## Installation
Ensure you have Python 3.x installed. 
No external libraries are strictly required for the core logic, but `traceroute` should be available on your system.

## Usage
Run the script from the terminal by providing a target IP:
```bash
python3 network_guard.py <remote_ip>
