import re

status_func = """
def launch_backend_status():
    h1("SuperBrain Status")
    
    token = "UNKNOWN"
    if TOKEN_FILE.exists():
        token = TOKEN_FILE.read_text(encoding="utf-8").strip()

    url = "NOT_FOUND"
    log_file = BACKEND_DIR / "config" / "localtunnel.log"
    if log_file.exists():
        match = re.search(r"your url is: (https://[^\s]+)", log_file.read_text(encoding="utf-8"))
        if match:
            url = match.group(1)
            
    if url == "NOT_FOUND":
        warn("Could not find a running localtunnel URL in config/localtunnel.log.")
        nl()
        print("  Wait 5 seconds, or run 'superbrain-server' to start the server.")
        return

    _display_connect_qr(url, token)
    
    local_url = "http://127.0.0.1:5000"
    local_ip = _detect_local_ip()
    network_url = f"http://{local_ip}:5000"
    
    nl()
    print(f"    Local URL      ?  {CYAN}{local_url}{RESET}")
    print(f"    Network URL    ?  {CYAN}{network_url}{RESET}")
    print(f"    Public URL   ?  {CYAN}{url}{RESET}  (localtunnel)")
    print(f"    API docs       ?  {CYAN}{local_url}/docs{RESET}")
    print(f"    Access Token   ?  {BOLD}{MAGENTA}{token}{RESET}")
    nl()
"""

for path in ['D:/superbrain/backend/start.py', 'D:/superbrain/superbrain-cli/payload/start.py']:
    content = open(path, 'r', encoding='utf-8').read()
    if 'def launch_backend_status()' not in content:
        content = content.replace('def main():', status_func + '\ndef main():')
        open(path, 'w', encoding='utf-8').write(content)
        print(f"Patched {path}")
    else:
        print(f"Already defined in {path}")
