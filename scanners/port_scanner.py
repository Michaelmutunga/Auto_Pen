import nmap
import json
import os

def scan_target(target):
    nm = nmap.PortScanner()
    print(f"[+] Scanning target: {target}")
    
    try:
        nm.scan(hosts=target, arguments='-sS -sV --top-ports 1000')

        if target in nm.all_hosts():
            results = {
                "target": target,
                "status": nm[target].state(),
                "protocols": {}
            }

            for proto in nm[target].all_protocols():
                results["protocols"][proto] = {}
                ports = nm[target][proto].keys()
                for port in sorted(ports):
                    results["protocols"][proto][port] = nm[target][proto][port]
            
            # Save results
            os.makedirs("results", exist_ok=True)
            with open(f"results/{target.replace('.', '_')}_scan.json", "w") as f:
                json.dump(results, f, indent=4)

            print(f"[+] Scan complete. Results saved to results/{target.replace('.', '_')}_scan.json")
            return results

        else:
            print("[-] Target not responsive.")
            return None

    except Exception as e:
        print(f"[-] Error during scan: {e}")
        return None

