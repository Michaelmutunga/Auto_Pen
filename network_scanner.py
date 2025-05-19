# network_scanner.py 

import nmap
import json
from exploit_matcher import match_exploits

scanner = nmap.PortScanner()

scan_results = []

target = input("\nEnter target IP or range (e.g., 192.168.1.0/24): ")
print(f"\n🔍 Scanning target: {target} ...\n")

scanner.scan(hosts=target, arguments='-sS -sV -O')

for host in scanner.all_hosts():
    print(f"Host: {host} ({scanner[host].hostname()})")
    print(f"State: {scanner[host].state()}")

    host_result = {
        "ip": host,
        "hostname": scanner[host].hostname(),
        "state": scanner[host].state(),
        "ports": [],
        "os": "Unknown"
    }

    if 'tcp' in scanner[host]:
        print("Protocol: tcp")
        for port in scanner[host]['tcp']:
            state = scanner[host]['tcp'][port]['state']
            name = scanner[host]['tcp'][port].get('name', '')
            product = scanner[host]['tcp'][port].get('product', '')
            version = scanner[host]['tcp'][port].get('version', '')
            print(f"  Port {port}: {state.upper()} - {name} ({product} {version})")

            host_result["ports"].append({
                "port": port,
                "state": state,
                "name": name,
                "product": product,
                "version": version
            })

            # Check for exploits
            matches = match_exploits(port, name, product)
            for match in matches:
                print(f"    ⚠  CVE Match: {match['cve']} - {match['desc']}")

    if 'osmatch' in scanner[host] and scanner[host]['osmatch']:
        top_os = scanner[host]['osmatch'][0]['name']
        host_result['os'] = top_os

        print("\nOS Detection:")
        for os in scanner[host]['osmatch']:
            print(f"  {os['name']} (Accuracy: {os['accuracy']}%)")

    scan_results.append(host_result)
    print("\n" + "-"*60 + "\n")

# Save results to a JSON file
with open("results/scan_results.json", "w") as outfile:
    json.dump(scan_results, outfile, indent=4)

print("✅ Scan results saved to results/scan_results.json")

