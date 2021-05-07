# HiddinWave Ver 1.0
# Powered by TechChip
# Secret Message Extractor
# from HiddenWave import encrypt
import os
import getpass
from sys import platform
import wave
import argparse
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from colorama import init
from termcolor import colored

init()

def decryptText(text,key):
    f = Fernet(key)
    return f.decrypt(text.encode())

def readKeyFromFile(filename):
    file = open(filename,'rb')
    key = file.read()
    file.close()
    return key

def createPasswordBasedKey():
    password = getpass.getpass('[INPUT] Enter Password for Decryption: ').encode()
    # password = input("[INPUT] Enter Password for Decryption: ").encode()
    saltpath = input("[INPUT] Enter Saved Salt File Location: ").encode()
    if not os.path.exists(saltpath):
      print("The Location you provided for the salt file is invalid or non-existstent. Please try again...")
      exit()
    with open(saltpath,'rb') as file:
      salt = file.read()
    print(colored("[SUCCESS]","green"),"Selected Salt:",salt)
    # print(colored("[WARNING]","red"),"Store the salt somewhere for creating the same key again!")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    print(colored("[SUCCESS]","green"),"Created the key for decryption!")
    print("Decrypting...")
    return key

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='audiofile', dest='audiofile')
parser.add_argument('-e', help='encrypted', dest='encrypted')
args = parser.parse_args()
af = args.audiofile
encrypted = args.encrypted
if encrypted == None:
  encrypted = 'N'
arged = False
if af:
    arged = True
def cls():
  if 'win32' in platform:
    os.system("cls")
  else:
    os.system("clear")
def help():
  print("\033[92mExtract Your Secret Message from Audio Wave File.\033[0m")
  print ('''usage: ExWave.py [-h] [-f AUDIOFILE] [-e Y/N]

optional arguments:
  -h, --help    show this help message and exit
  -f AUDIOFILE  Select Audio File
  -e Encrypted [Y/N] Is the message Encrypted?''')
  
def banner():
    print ('''
 _  _ _    _    _         __      __
| || (_)__| |__| |___ _ _ \ \    / /_ ___ _____
| __ | / _` / _` / -_) ' \ \ \/\/ / _` \ V / -_)
|_||_|_\__,_\__,_\___|_||_|_\_/\_/\__,_|\_/\___|
                         |___|v1.0 \033[1;91mwww.techchip.net\033[0m
\033[92mVisit for more tutorials : www.youtube.com/techchipnet\033[0m
\033[93mHide your text message in wave audio file like MR.ROBOT\033[0m''')

def ex_msg(af):
    if not arged:
      help()
    else:
        print ("Please wait...")
        waveaudio = wave.open(af, mode='rb')
        frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
        extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
        string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
        msg = string.split("###")[0]
        if encrypted.upper() == 'Y':
          # msg.encode()
          print("The message is encrypted, do you have the Key File?")
          choice = input("[1] I have key file\n[2] I have the salt and password for the key\nSelection > ")
          if choice == '1':
            keypath = input("Enter the complete path to the key file\nNote: Use '/' instead of '\\' if you are on Windows\nPath: ")
            if os.path.exists(keypath):
              key = readKeyFromFile(keypath)
              msg = decryptText(msg,key)
            else:
              print("The location for the key you provided is invalid. Check the path and try again.")
          elif choice == '2':
            key = createPasswordBasedKey()
            msg = decryptText(msg,key)
          else:
            print("{} isn't a valid option. Please choose among 1 and 2 only.")
            if input("Try again? [Y/N] > ").upper() == 'Y':
              ex_msg(af)
        print("Your Secret Message is: \033[1;91m"+msg.decode()+"\033[0m")
        waveaudio.close()
cls()
banner()
ex_msg(af)
try:
  ex_msg(af)
except:
  print ("Something went wrong!! try again")
quit('')
