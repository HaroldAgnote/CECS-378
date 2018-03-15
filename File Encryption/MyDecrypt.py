import os
import json
import base64
import constants
from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def MyDecrypt(cipherText, key, IV):
    # Default backend for Cipher usage
    backend = default_backend()

    # Set up cipher with AES-CBC and the previously used key and IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(IV), backend = backend)

    # Decrypt
    decryptor = cipher.decryptor()
    paddedMessage = decryptor.update(cipherText) + decryptor.finalize()

    # Unpad the decrypted bytes
    unpadder = padding.PKCS7(constants.CBC_BLOCK_LENGTH).unpadder()
    plainText = unpadder.update(paddedMessage) + unpadder.finalize()

    # Return plain-text
    return plainText

def MyFileDecrypt(filePath):
    # Verify filepath is a file
    if(not os.path.isfile(filePath)):
        print("File not found")
    else:
        # Initialize variables
        cipherText = ""
        IV = ""
        key = ""
        ext = ""

        fileName = filePath.rsplit(".", 1)[0]

        jsonFileName = fileName + ".json"

        # Extract data from json file
        with open(jsonFileName) as f:    
           data = json.load(f)
           cipherText = b64decode(data["Cipher Text"])
           IV = b64decode(data["IV"])
           key = b64decode(data["Key"])
           ext = data["Extension"]

        # Decrypt the file
       	plainText = MyDecrypt(cipherText, key, IV)

       	# Write the results
        file = open(filePath, 'wb')
        file.write(plainText)
        print("Results of decryption stored at: decryptedFile" + ext)
