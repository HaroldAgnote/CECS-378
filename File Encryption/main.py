import os
import json
from base64 import b64encode
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import MyEncrypt
import MyDecrypt
import constants

def genRSAKey():
	privateKey = rsa.generate_private_key(public_exponent = 65537, key_size = 2048, backend = default_backend())
	with open("privateKey.pem", 'w') as f:
		f.write(privateKey)
	publicKey = privateKey.publicKey()
	with open("publicKey.pem", 'w') as f:
		f.write(publicKey)

# Allows the user to input a filepath of a file to encrypt/decrypt
repeat = True
while(repeat):
    print("File Encryptor/Decryptor")
    print("---------------------------")
    print("1. Encrypt a file")
    print("2. Decrypt a file")
    print("3. Exit")
    selection = str(input())
    if selection == "1":
        # Get user input for the file
        #input("Enter the filepath for the file to be encrypted (e.g. larry.jpg): ")
        filePath = "files/larry.jpg"

        # Generate private/public key
        genRSAKey()

        # Call the encryptor
        cipherText, IV, key, ext = MyEncrypt.MyRSAEncrypt(filePath = filePath, RSAPublicKeyFilePath = "publicKey.pem")

        #Create the dictionary
        jsonData = {"Cipher Text": b64encode(cipherText).decode('utf-8'), "IV": b64encode(IV).decode('utf-8'), "Key": b64encode(key).decode('utf-8'), "Extension": ext}

        fileName = filePath.rsplit(".", 1)[0]

        # Create json file from dictionary
        jsonFileName = fileName + ".json"
        with open(jsonFileName, 'w') as outfile:
            json.dump(jsonData, outfile)
        print("Results of encryption stored at: " + jsonFileName)
    elif selection == "2":
        # Get user input for encrypted file
        filePath = input("Enter the filepath for the file to be decrypted: ")

        # Decrypt the encrypted message
        MyDecrypt.MyFileDecrypt(filePath)
    elif selection == "3":
        print("Exiting")
        repeat = False
    else:
        print("Invalid input")

os.system("pause")
