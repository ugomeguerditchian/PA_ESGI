import os
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

#Génération des clefs privé / public
global key
global private_key

def rsa_decrypt(data_to_decrypt):
    rsa_private_key = RSA.importKey(private_key)
    rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
    decrypted_text = rsa_private_key.decrypt(data_to_decrypt)

    return(decrypted_text)

#Récupération de la private key RSA
content_file = open("/encrypt/private.key", 'rb')
private_key = content_file.read()
content_file.close


#Ouverture du fichier chiffré
path_file = "test_excel.xlsx"
file = open(path_file, "rb")
#Lecture du fichier chiffré
byte = file.read()
len_encrypted_file = size_of_file = os.path.getsize(path_file)
file.close()
div_RSA_table =[]
unit_RSA = 0
print(len_encrypted_file)

if len_encrypted_file > 256 :
    range_pourc = int(len_encrypted_file / 256) + (len_encrypted_file % 256 > 0)
    print(range_pourc)
    for i in range(range_pourc):
        if unit_RSA+256 > len_encrypted_file:
            diffe = len_encrypted_file-(range_pourc*256) + 256
            div_RSA_table.append(byte[unit_RSA:unit_RSA+diffe])
        else:
            div_RSA_table.append(byte[0+unit_RSA:unit_RSA+256])
            unit_RSA += 256
else :
    div_RSA_table.append(byte[unit_RSA:len_encrypted_file])
    range_pourc = 1

encrypted_part = []
for i in range(range_pourc):
    encrypted_part.append(rsa_decrypt(div_RSA_table[i]))

encrypted_part2 = b''.join(encrypted_part)
file = open(path_file, "wb")
file.write(encrypted_part2)
file.close
print("closed")
