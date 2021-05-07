# HiddinWave Ver 1.0
# Powered by TechChip
# Hide your secret text in wave audio file.
import os
from sys import platform
import getpass
import wave
import argparse
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from colorama import init
from termcolor import colored

init()

def createRandomKey():
    key = Fernet.generate_key()
    print(colored("[SUCCESS]","green"),"Created Key: ",key)
    print(colored("[WARNING]","red"),"Store Key for Decrypting!")
    return key

def saveKeyToFile(filename,key):
    file = open(filename,'wb')
    file.write(key)
    file.close()

def readKeyFromFile(filename):
    file = open(filename,'rb')
    key = file.read()
    file.close()
    return key

def createPasswordBasedKey():
    password = getpass.getpass("[INPUT] Enter Password for Encryption: ").encode()
    # password = input("[INPUT] Enter Password for Encryption: ").encode()
    choice = input("[SELECTION] Choose Salt Type:\n   [1] Custom\n   [2] Random")
    if choice=="1":
        salt = input("Enter Custom Salt: ").encode()
    else:
        salt = os.urandom(16)
    print(colored("[SUCCESS]","green"),"Created Salt:",salt)
    print(colored("[WARNING]","red"),"Store the salt somewhere for creating the same key again!")
    print(colored("[WARNING]","yellow"),"Please provide a name for saving the Salt File: ")
    saltPath = input("> ")
    if os.path.exists(saltPath):
      print("The file already exists, would you like to replace it?")
      if input("[Y/N] ---> ").upper() != 'Y':
        print(colored("[WARNING]","yellow"),"Please provide a name for saving the Salt File: ")
        saltPath = input("> ")
    with open(saltPath + '.salt','wb') as file:
      file.write(salt)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    print(colored("[SUCCESS]","green"),"Created Key: ",key)
    return key

def encryptText(text,key):
    f = Fernet(key)
    return f.encrypt(text.encode())

def chooseEncryptionType():
    # choice = input(colored("[SELECTION]","yellow"),"Type of Encryption Key:\n   [1] Random Key\n   [2] Password Based Key\nSelection > ")
    choice = input("Type of Encryption Key:\n   [1] Random Key\n   [2] Password Based Key\nSelection > ")
    if choice=="1":
        return createRandomKey()
    else:
        return createPasswordBasedKey()

def encrypt(string):
  choice = input('Select option:\n[1] Use a pre-made key file for encryption\n[2] Create a new Key File and use that\n> ')
  if choice=='1':
    keypath = input("Enter the complete location of the key file: ")
    if os.path.exists(keypath):
      key = readKeyFromFile(keypath)
      return encryptText(string, key)
    else:
      print("The path you provided isn't either correct or doesn't exist")
  elif choice=='2':
    key = chooseEncryptionType()
    print("Saving the key...")
    filename = input("What name would you like to give to the key file: ")
    saveKeyToFile(filename, key)
    return(encryptText(string, key))
  else:
    print("You can either choose 1 or 2. {} isn't a valid choice".format(choice))
    if input("Try again? [Y/N]: ").upper() == 'Y':
      encrypt(string)

parser = argparse.ArgumentParser()
parser.add_argument('-f', help='Select Audio File', dest='audiofile')
parser.add_argument('-m', help='Enter your Secret Message', dest='secretmsg')
parser.add_argument('-o', help='Your Output file path and name', dest='outputfile')
parser.add_argument('-e', help='Encrypt your message [Y/N]', dest='encryptPrompt')
args = parser.parse_args()
af = args.audiofile
string = args.secretmsg
encchoice = args.encryptPrompt
if encchoice != None:
  if encchoice.upper() == 'Y':
    string = encrypt(string).decode()
output = args.outputfile
arged = False
if af and string and output:
    arged = True
def cls():
  if 'win32' in platform:
    os.system("cls")
  else:
    os.system("clear")
def help():
  print("\033[92mHide Your Secret Message in Audio Wave File.\033[0m")
  print ('''usage: HiddenWave.py [-h] [-f AUDIOFILE] [-m SECRETMSG] [-o OUTPUTFILE]

optional arguments:
  -e, --encrypt Encrypt the message using Symmetric Key [Y/N]
  -h, --help    show this help message and exit
  -f AUDIOFILE  Select Audio File
  -m SECRETMSG  Enter your message
  -o OUTPUTFILE Your output file path and name''')
  
def banner():
    print ('''
 _  _ _    _    _         __      __
| || (_)__| |__| |___ _ _ \ \    / /_ ___ _____
| __ | / _` / _` / -_) ' \ \ \/\/ / _` \ V / -_)
|_||_|_\__,_\__,_\___|_||_|_\_/\_/\__,_|\_/\___|
                         |___|v1.0 \033[1;91mwww.techchip.net\033[0m
\033[92mVisit for more tutorials : www.youtube.com/techchipnet\033[0m
\033[93mHide your text message in wave audio file like MR.ROBOT\033[0m''')

def em_audio(af, string, output):
    if not arged:
      help()
    else:
      print ("Please wait...")
      waveaudio = wave.open(af, mode='rb')
      frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
      string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
      bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
      for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
      frame_modified = bytes(frame_bytes)
      with wave.open(output, 'wb') as fd:
        fd.setparams(waveaudio.getparams())
        fd.writeframes(frame_modified)
      waveaudio.close()
      print ("Done...")
cls()
banner()
try:
  em_audio(af, string, output)
except:
  print ("Something went wrong!! try again")
  quit('')
