#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from UI.indicators import print_info, print_warning, print_success


def is_admin():
    if os.name == 'nt':
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    else:
        return os.geteuid() == 0


if not is_admin():
    print_warning("Not running as root/admin. Please re-run as administrator.")
    sys.exit(1)

print_info("Running TOR setup...")
exit_code = os.system(f"{sys.executable} TOR_Setup.py")
if exit_code != 0:
    print_warning("TOR setup failed.")
    sys.exit(exit_code)

print_info("Running Python setup...")
exit_code = os.system(f"{sys.executable} Python_Setup.py")
if exit_code != 0:
    print_warning("Python setup failed.")
    sys.exit(exit_code)

print_success("All setup scripts completed successfully.")
