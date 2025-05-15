from pymetasploit3.msfrpc import MsfRpcClient

client = MsfRpcClient('password123', username='msf', port=55553, ssl=False)

print(f"[+] Connected to Metasploit - Console ID: {client.consoles.console().cid}")

