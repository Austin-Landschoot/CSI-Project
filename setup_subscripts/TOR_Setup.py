#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
import tarfile
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from UI.indicators import print_warning, print_success, print_info, print_prompt

# I am only familiar with apt so other tor install commands may not work.
managers = {
    "apt": f"sudo apt update && sudo apt install -y tor",
    "dnf": f"sudo dnf install -y tor",
    "yum": f"sudo yum install -y tor",
    "pacman": f"sudo pacman -Sy --noconfirm tor",
    "zypper": f"sudo zypper install -y tor"
}


def get_valid_port(prompt_text, default):
    while True:
        port = input(print_prompt(f"{prompt_text} (default: {default}): ")) or default
        if port.isdigit() and 1 <= int(port) <= 65535:
            return port
        else:
            print_warning("Please enter a valid port number between 1 and 65535.")


def install_tor_unix():
    for manager, command in managers.items():
        if shutil.which(manager):
            print_info(f"Using package manager: {manager}")
            subprocess.run(command, shell=True)
            print_success("TOR installed.")
            break
    else:
        print_warning("No supported package manager found.")
        sys.exit(1)

    c2_port = get_valid_port("Port for hidden service (C2 listener, Default: 4444)", "4444")
    socks_port = get_valid_port("Local SOCKS port (for outgoing proxy, Default: 9050)", "9050")

    torrc_path = "/etc/tor/torrc"
    tor_service_dir = "/var/lib/tor/my_hidden_service"

    config = f"""SOCKSPort {socks_port}
HiddenServiceDir {tor_service_dir}
HiddenServicePort {c2_port} 127.0.0.1:{c2_port}
"""

    with open(torrc_path, "w") as file:
        file.write(config)
    print_info(f"Edited {torrc_path} configuration file.")

    subprocess.run("sudo systemctl restart tor", shell=True)
    print_success("TOR service restarted.")

    hostname_path = os.path.join(tor_service_dir, "hostname")
    if os.path.exists(hostname_path):
        onion = open(hostname_path).read().strip()
        print_success(f"Your hidden service address: {onion}:{c2_port}")
    else:
        print_warning("Could not read .onion address. It may take a few seconds to generate.")


def install_tor_windows():
    print_info("Extracting TOR Expert Bundle...")
    bundle_path = os.path.join(os.path.dirname(__file__), "tor-expert-bundle-windows-x86_64-13.5.16.tar.gz")
    try:
        with tarfile.open(bundle_path, "r:gz") as tar:
            tar.extractall("TOR")
        print_success("TOR extracted.")
    except tarfile.TarError:
        print_warning("Invalid TOR archive.")
        sys.exit(1)

    c2_port = get_valid_port("Port for hidden service (C2 listener, Default: 4444)", "4444")
    socks_port = get_valid_port("Local SOCKS port (for outgoing proxy, Default: 9050)", "9050")

    base_path = os.path.join(os.getcwd(), "TOR", "tor")
    torrc_path = os.path.join(base_path, "torrc")
    tor_data_dir = os.path.join(base_path, "data")
    hidden_service_dir = os.path.join(tor_data_dir, "my_hidden_service")
    os.makedirs(hidden_service_dir, exist_ok=True)

    config = f"""SOCKSPort {socks_port}
DataDirectory {tor_data_dir}
HiddenServiceDir {hidden_service_dir}
HiddenServicePort {c2_port} 127.0.0.1:{c2_port}
"""

    with open(torrc_path, "w") as file:
        file.write(config)
    print_success(f"Wrote torrc to: {torrc_path}")

    tor_exe = os.path.join(base_path, "tor.exe")
    print_info("Starting TOR with custom config...")
    subprocess.Popen(
        [tor_exe, "-f", torrc_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        )
    print_success("TOR started.")

    hostname_path = os.path.join(hidden_service_dir, "hostname")
    print_info("Waiting for hidden service address...")

    for _ in range(10):
        if os.path.exists(hostname_path):
            onion = open(hostname_path).read().strip()
            print_success(f"Your hidden service address: {onion}:{c2_port}")
            break
        time.sleep(1)
    else:
        print_warning("Could not read .onion address. It may take a few seconds to generate.")


def main():
    if os.name == "posix":
        install_tor_unix()
    elif os.name == "nt":
        install_tor_windows()
    else:
        print_warning("Unsupported OS.")
        sys.exit(1)

main()
