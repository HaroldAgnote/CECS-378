import os
import json
from base64 import b64encode
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import MyEncrypt
import MyDecrypt
import constants

def genRSAKey():
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
	with open("privateKey.pem", 'wb') as f:
		f.write(privatePEM)
	publicKey = privateKey.public_key()
	publicPEM = publicKey.public_bytes(
		encoding = serialization.Encoding.PEM,
		format = serialization.PublicFormat.SubjectPublicKeyInfo
	)
	with open("publicKey.pem", 'wb') as f:
		f.write(publicPEM)

# Allows the user to input a filepath of a file to encrypt/decrypt
repeat = True
while(repeat):
	print("File Encryptor/Decryptor")
	print("---------------------------")
	print("1. Encrypt a file")
	print("2. Decrypt a file")
	print("3. Exit")
	selection = input()
	if selection == "1":
		# Get user input for the file
		filePath = input("Enter the filepath for the file to be encrypted (e.g. files/larry.jpg): ")

		# Generate private/public key if it does not already exist
		if((not os.path.isfile(constants.PUBLIC_KEY_FILE_PATH)) or (not os.path.isfile(constants.PRIVATE_KEY_FILE_PATH))):
			genRSAKey()

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
	elif selection == "2":
		# Get user input for encrypted file
		filePath = input("Enter the filepath for the file to be decrypted (e.g. files/larry.json): ")

		# Set the private key filepath
		RSAPrivateKeyFilePath = constants.PRIVATE_KEY_FILE_PATH

		# Decrypt the encrypted message
		MyDecrypt.MyRSADecryptMAC(filePath, RSAPrivateKeyFilePath)
	elif selection == "3":
		print("Exiting")
		repeat = False
	else:
		print("Invalid input")

os.system("pause")
