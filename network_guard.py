import subprocess
import os
import re
import ipaddress
import sys
from datetime import datetime

class NetworkGuard:
    def __init__(self, target, base_path="scans"):
        self.target = target
        self.stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = os.path.join(base_path, f"target_{target}_{self.stamp}")

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def run_cmd(self, label, cmd):
        print(f"[+] Task: {label}")
        path = os.path.join(self.output_dir, f"{label}.log")

        try:
            # Execute shell command and capture streams
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            with open(path, "w") as f:
                f.write(f"--- {label.upper()} ---\n{res.stdout}")
                if res.stderr:
                    f.write(f"\n--- ERRORS ---\n{res.stderr}")

            return res.stdout
        except Exception as e:
            print(f"[!] Fail: {e}")
            return None

    def parse_net(self, data):
        results = {}
        curr = None

        for line in data.splitlines():
            line = line.strip()

            # Interface identification
            if_match = re.search(r"^\d+: ([^:]+)", line)
            if if_match:
                curr = if_match.group(1)
                results[curr] = {"ip": None, "mac": None, "net": None}
                continue

            if not curr: continue

            # Hardware address extraction
            mac = re.search(r"link/\S+\s+([0-9a-f:]{17})", line)
            if mac: results[curr]["mac"] = mac.group(1)

            # IPv4/CIDR extraction and network calculation
            ip_m = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)/(\d+)", line)
            if ip_m:
                ip, cidr = ip_m.group(1), ip_m.group(2)
                try:
                    network = ipaddress.ip_network(f"{ip}/{cidr}", strict=False)
                    results[curr].update({"ip": ip, "net": str(network.network_address)})
                except: pass
        
        return results

if __name__ == "__main__":
    # Argument handling
    if len(sys.argv) > 1:
        target_ip = sys.argv[1]
    else:
        print("[!] No target provided. Usage: python3 network_guard.py <remote_ip>")
        sys.exit(1)

    guard = NetworkGuard(target_ip)

    # Internal Audit: Capture host state
    local_raw = guard.run_cmd("local_audit", "ip addr")
    if local_raw:
        summary = guard.parse_net(local_raw)
        print(f"[*] Local context captured ({len(summary)} interfaces)")

    # External Recon: Connectivity and route path
    guard.run_cmd("remote_ping", f"ping -c 4 {target_ip}")
    guard.run_cmd("remote_path", f"traceroute {target_ip}")

    # Output report
    print("\n" + "=" * 80)
    print(f"{'INTERFACE':<15} | {'IP ADDRESS':<15} | {'MAC ADDRESS':<20} | {'NETWORK'}")
    print("-" * 80)
    
    if local_raw:
        for name, info in summary.items():
            ip_val = info["ip"] if info["ip"] else "N/A"
            mac_val = info["mac"] if info["mac"] else "N/A"
            net_val = info["net"] if info["net"] else "N/A"
            print(f"{name:<15} | {ip_val:<15} | {mac_val:<20} | {net_val}")
    
    print("=" * 80 + f"\n[OK] Logs stored in: {guard.output_dir}\n")
