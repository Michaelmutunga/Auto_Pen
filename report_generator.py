import json

def generate_report(target_ip, exploit_name, payload_name, status):
    report = {
        'target_ip': target_ip,
        'exploit': exploit_name,
        'payload': payload_name,
        'status': status
    }
    
    with open('exploit_report.json', 'a') as f:
        json.dump(report, f)
        f.write('\n')

def main():
    # Example usage
    target_ip = '192.168.100.73'
    exploit_name = 'exploit/windows/smb/ms17_010_eternalblue'
    payload_name = 'windows/meterpreter/reverse_tcp'
    status = 'success'  # This would be determined dynamically in the exploit process

    generate_report(target_ip, exploit_name, payload_name, status)

if __name__ == '__main__':
    main()

