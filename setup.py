import os
import sys
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


def running_from_project_directory():
    current_dir = os.path.basename(os.getcwd())
    if current_dir != "fsoc.C2":
        return False
    else:
        return True


if not running_from_project_directory():
    print_warning("Setup must be run in the fsoc.C2 directory.")
    sys.exit(1)

if not is_admin():
    print_warning("Not running as root/admin. Please re-run as administrator.")
    sys.exit(1)

print_info("Running TOR setup...")
exit_code = os.system(f"{sys.executable} setup_subscripts/TOR_Setup.py")
if exit_code != 0:
    print_warning("TOR setup failed.")
    sys.exit(exit_code)

print_info("Running Python setup...")
exit_code = os.system(f"{sys.executable} setup_subscripts/Python_Setup.py")
if exit_code != 0:
    print_warning("Python setup failed.")
    sys.exit(exit_code)

print_success("All setup scripts completed successfully.")
