import os
import json
import base64
import constants
from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as apadding
from cryptography.hazmat.primitives import padding, serialization, hashes
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

        jsonFile = open(jsonFileName, 'rb')

        # Extract data from json file
        data = json.load(jsonFile)

        cipherText = b64decode(data["Cipher Text"])
        IV = b64decode(data["IV"])
        key = b64decode(data["Key"])
        ext = data["Extension"]

        # Decrypt the file
        plainText = MyDecrypt(cipherText, key, IV)

        # Write the results
        file = open(filePath, 'wb')
        file.write(plainText)
        print("Results of decryption stored at: " + filePath)

def MyRSADecrypt(filePath, RSAPrivateKeyFilePath):
    if(not os.path.isfile(filePath)):
        print("File not found")
    else:
        # Initialize variables
        cipherText = ""
        IV = ""
        RSAkey = ""
        ext = ""
        privateKey = ""

        # Extract data from json file
        with open(filePath) as f:
            data = json.load(f)
            cipherText = b64decode(data["Cipher Text"])
            IV = b64decode(data["IV"])
            RSAkey = data["Key"]
            ext = data["Extension"]

        # Convert RSA key to AES key
        with open(RSAPrivateKeyFilePath, "rb") as key_file:
            privateKey = serialization.load_pem_private_key(
                key_file.read(),
                password = None,
                backend = default_backend()
            )

        key = privateKey.decrypt(
            RSAkey,
            apadding.OAEP(
                mgf = apadding.MGF1(algorithm = hashes.SHA256),
                algorithm = hashes.SHA256,
                label = None
            )
        )

        #Create the dictionary
        jsonData = {"Cipher Text": b64encode(cipherText).decode('utf-8'), "IV": b64encode(IV).decode('utf-8'), "Key": b64encode(key).decode('utf-8'), "Extension": ext}
        fileName = filePath.rsplit(".", 1)[0]


        # Create json file from dictionary
        jsonFileName = fileName + ".json"
        with open(jsonFileName, 'w') as outfile:
            json.dump(jsonData, outfile)

        # Pass new json file to MyFileEncrypt
        MyFileEncrypt(jsonFileName)
