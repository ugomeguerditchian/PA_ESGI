import os
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

key = RSA.generate(2048)

#export des clefs privé/public
content_file = open("/encrypt/private.key", 'wb')
content_file.write(key.exportKey('PEM'))
content_file.close
public_key = key.publickey()
content_file = open("/encrypt/public.key", 'wb')
content_file.write(public_key.exportKey('OpenSSH'))
content_file.close

content_file = open("/encrypt/public.key", 'rb')
public_key = content_file.read()
content_file.close
