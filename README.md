# NetworkGuard

A lightweight Python tool for automated network reconnaissance and local system auditing. Built for security researchers to capture environment snapshots during target scans.

## 🐧 Compatibility
**Note:** This tool is designed for **Linux-based systems**. It relies on `iproute2` and `traceroute` utilities which are standard in Linux environments (Ubuntu, Debian, Kali, etc.).

- **Windows Users**: Use **WSL2** (Windows Subsystem for Linux) to run this tool.
- **macOS Users**: May require manual installation of `traceroute`.

## 🛠 Features
- **Host Audit**: Logs local interface states (IP, MAC, Network) before remote scans.
- **Remote Recon**: Automates connectivity checks and path tracing to a target IP.
- **Log Management**: Automatically organizes results into timestamped directories.
- **Data Parsing**: Uses Regex to extract structured network data from raw `ip addr` output.

## 🔧 Requirements
- **Python 3.x**
- **System Utilities**: `iproute2` (for `ip addr` command) and `traceroute`.
- No external Python libraries required (uses native `subprocess`, `re`, and `ipaddress`).

## 🚀 Usage
Run the script from the terminal by providing a target IP:

```bash
python3 network_guard.py <remote_ip>
