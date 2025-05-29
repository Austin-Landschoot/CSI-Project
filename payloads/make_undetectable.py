#!/usr/bin/env python3
import os
import argparse
import argcomplete
from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms
from cryptography.hazmat.backends import default_backend
from UI.indicators import print_warning, print_success, print_prompt


def encrypt(data):
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data.encode('utf-8')) + encryptor.finalize()
    return key, iv + encrypted


def modify_script(input_file, output_file, switches):
    with open(input_file, 'r') as file:
        code = file.read()

    key, encrypted_script = encrypt(code)
    encrypted_script_repr = repr(encrypted_script)
    key_repr = repr(key)

    modified_code = f"""
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def decrypt(data, key_value):
    iv = data[:16]
    encrypted_data = data[16:]
    cipher = Cipher(algorithms.AES(key_value), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data) + decryptor.finalize()

encrypted_payload = {encrypted_script_repr}
decryption_key = {key_repr}

exec(decrypt(encrypted_payload, decryption_key).decode())
"""

    if 'disable_new_file' in switches:
        with open(input_file, 'w') as file:
            file.write(modified_code)
        print_success(f"Script modified in place: {input_file}")
    elif output_file:
        with open(output_file, 'w') as file:
            file.write(modified_code)
        print_success(f"Encrypted script saved to: {output_file}")

    if 'remote_key' in switches:
        store_key_remotely(key)


def store_key_remotely(key):
    # Placeholder for remote key
    pass


def main():
    parser = argparse.ArgumentParser(
        description='Encrypt Python scripts using AES encryption for security and obfuscation.'
    )

    parser.add_argument('script_path', nargs='?', type=str,
                        help='Path to the script to be encrypted (positional argument).')
    parser.add_argument('output_path', nargs='?', type=str,
                        help='Path to the output file (positional argument).')

    parser.add_argument('-s', '--script', type=str,
                        help='Specify the path to the script to be encrypted (optional flag).')
    parser.add_argument('-o', '--output', type=str, default="modified_payload.py",
                        help='Specify the output file name (default: "modified_payload.py").')

    parser.add_argument('-d', '--disable-new-file', action='store_true',
                        help='Modify the specified script in place without generating a new file.')
    parser.add_argument('-r', '--remote-key', action='store_true',
                        help='Store the decryption key on a remote server for additional security.')

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    input_script = args.script_path or args.script
    output_script = args.output_path or args.output

    if not input_script:
        input_script = input(print_prompt("Enter the path to the script file: "))

    while not os.path.isfile(input_script):
        print_warning('Invalid file path.')
        input_script = input(print_prompt("Enter a valid script file path: "))

    switches = []
    if args.disable_new_file:
        switches.append('disable_new_file')
    if args.remote_key:
        switches.append('remote_key')

    modify_script(input_script, output_script, switches)


if __name__ == '__main__':
    main()
