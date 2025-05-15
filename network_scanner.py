# network_scanner.py

import nmap
from exploit_matcher import match_exploits

scanner = nmap.PortScanner()

target = input("\nEnter target IP or range (e.g., 192.168.1.0/24): ")
print(f"\n🔍 Scanning target: {target} ...\n")

scanner.scan(hosts=target, arguments='-sS -sV -O')

for host in scanner.all_hosts():
    print(f"Host: {host} ({scanner[host].hostname()})")
    print(f"State: {scanner[host].state()}")

    if 'tcp' in scanner[host]:
        print("Protocol: tcp")
        for port in scanner[host]['tcp']:
            state = scanner[host]['tcp'][port]['state']
            name = scanner[host]['tcp'][port].get('name', '')
            product = scanner[host]['tcp'][port].get('product', '')
            version = scanner[host]['tcp'][port].get('version', '')
            print(f"  Port {port}: {state.upper()} - {name} ({product} {version})")

            # Check for exploits
            matches = match_exploits(port, name, product)
            for match in matches:
                print(f"    ⚠️  CVE Match: {match['cve']} - {match['desc']}")

    if 'osmatch' in scanner[host]:
        print("\nOS Detection:")
        for os in scanner[host]['osmatch']:
            print(f"  {os['name']} (Accuracy: {os['accuracy']}%)")

    print("\n" + "-"*60 + "\n")

