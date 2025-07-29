#!/usr/bin/env python3
"""
set_printer_language.py
Switch a Creality Ender‑3 V3 Plus (Creality OS) display to English.

Usage:
    python set_printer_language.py --host 192.168.1.123 \
                                   --user root \
                                   --password Creality2023
"""
import argparse
import datetime as dt
import json
import os
import tempfile
import paramiko


REMOTE_JSON = "/usr/data/creality/userdata/config/system_config.json"
LANG_VALUE = 1                     # 0 = Chinese, 1 = English

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Set printer UI language to English")
    p.add_argument("--host", required=True, help="Printer IP / hostname")
    p.add_argument("--user", required=True, help="SSH username (root)")
    p.add_argument("--password", help="SSH password (omit if key auth)")
    p.add_argument("--port", type=int, default=22, help="SSH port (default 22)")
    return p.parse_args()

def ssh_connect(host: str, port: int, user: str, pw: str | None) -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port=port, username=user, password=pw, timeout=10)
    return client

def backup_remote_file(ssh: paramiko.SSHClient, path: str) -> None:
    ts = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = f"{path}.bak.{ts}"
    cmd = f"cp {path} {backup_path}"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    if stdout.channel.recv_exit_status() != 0:
        raise RuntimeError(f"Backup failed: {stderr.read().decode().strip()}")
    print(f"✔ Backup created → {backup_path}")

def fetch_file(sftp: paramiko.SFTPClient, remote: str) -> str:
    local_tmp = tempfile.NamedTemporaryFile(delete=False)
    local_tmp.close()
    sftp.get(remote, local_tmp.name)
    return local_tmp.name

def push_file(sftp: paramiko.SFTPClient, local_path: str, remote_path: str) -> None:
    sftp.put(local_path, remote_path)

def modify_language(local_json_path: str, lang_value: int) -> None:
    with open(local_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "user_info" not in data:
        raise KeyError("'user_info' key not found in JSON")

    data["user_info"]["language"] = lang_value

    with open(local_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def restart_ui(ssh: paramiko.SSHClient) -> None:
    # The UI process name can differ by firmware build; try both variants:
    ssh.exec_command("pkill -f crealityui || pkill -f creality-launcher || true")

def main() -> None:
    args = parse_args()
    ssh = ssh_connect(args.host, args.port, args.user, args.password)
    sftp = ssh.open_sftp()

    try:
        print("→ Backing up JSON …")
        backup_remote_file(ssh, REMOTE_JSON)

        print("→ Downloading JSON …")
        local_json = fetch_file(sftp, REMOTE_JSON)

        print("→ Modifying language …")
        modify_language(local_json, LANG_VALUE)

        print("→ Uploading modified JSON …")
        push_file(sftp, local_json, REMOTE_JSON)

        print("→ Restarting UI …")
        restart_ui(ssh)

        print("Done! Screen should reload in English.")
    finally:
        sftp.close()
        ssh.close()
        if 'local_json' in locals() and os.path.isfile(local_json):
            os.unlink(local_json)

if __name__ == "__main__":
    main()
