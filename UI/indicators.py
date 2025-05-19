from colorama import Fore, Style, init

init(autoreset=True)


def print_info(text):
    print(f"{Fore.WHITE}{Style.BRIGHT}[{Fore.YELLOW}*{Fore.WHITE}]{Fore.YELLOW} {text}{Style.RESET_ALL}")


def print_prompt(text):
    return f"{Fore.WHITE}{Style.BRIGHT}[{Fore.CYAN}?{Fore.WHITE}]{Fore.WHITE} {text}{Style.RESET_ALL}"


def print_warning(text):
    print(f"{Fore.WHITE}{Style.BRIGHT}[{Fore.RED}!{Fore.WHITE}]{Fore.RED} {text}{Style.RESET_ALL}")


def print_success(text):
    print(f"{Fore.WHITE}{Style.BRIGHT}[{Fore.GREEN}+{Fore.WHITE}]{Fore.GREEN} {text}{Style.RESET_ALL}")
