import os
import json
from src import constants
from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding as apadding
from cryptography.hazmat.primitives import padding, serialization, hashes, hmac
from cryptography.hazmat.backends import default_backend

def MyDecryptMAC(cipherText, IV, tag, EncKey, HMACKey):
	# Default backend for Cipher usage
	backend = default_backend()

	#Check Tags
	tagCheck = hmac.HMAC(HMACKey, hashes.SHA256(), backend = backend)
	tagCheck.update(cipherText)
	try:
		tagCheck.verify(tag)

		# Set up cipher with AES-CBC and the previously used key and IV
		cipher = Cipher(algorithms.AES(EncKey), modes.CBC(IV), backend = backend)

		# Decrypt
		decryptor = cipher.decryptor()
		paddedMessage = decryptor.update(cipherText) + decryptor.finalize()

		# Unpad the decrypted bytes
		unpadder = padding.PKCS7(constants.CBC_BLOCK_LENGTH).unpadder()
		plainText = unpadder.update(paddedMessage) + unpadder.finalize()

		# Return plain-text
		return plainText
	except InvalidSignature:
		print("Invalid tag")
		return None

def MyFileDecryptMAC(fileName, cipherText, IV, tag, EncKey, HMACKey, ext):
	# Decrypt the file
	plainText = MyDecryptMAC(cipherText, IV, tag, EncKey, HMACKey)


	# Write the results
	filePath = fileName + ext
	file = open(filePath, 'wb')
	file.write(plainText)
	print("Results of decryption stored at: " + filePath)

def MyRSADecryptMAC(filePath, RSAPrivateKeyFilePath):
	if(not os.path.isfile(RSAPrivateKeyFilePath)):
			print("RSA Private Key File not found")
	else:
		# Initialize variables
		RSACipher = ""
		cipherText = ""
		IV = ""
		tag = ""
		ext = ""
		privateKey = ""

		# Extract data from json file
		fileName = filePath.rsplit(".", 1)[0]
		jsonFileName = fileName + ".json"
		jsonFile = open(jsonFileName, "r")

		data = json.load(jsonFile)

		RSACipher = b64decode(data["RSACipher"][0])
		cipherText = b64decode(data["Cipher Text"][0])
		IV = b64decode(data["IV"][0])
		tag = b64decode(data["Tag"][0])
		ext = data["Extension"]

		# Convert RSA key to EncKey and HMACKey
		with open(RSAPrivateKeyFilePath, "rb") as key_file:
			privateKey = serialization.load_pem_private_key(
				key_file.read(),
				password = None,
				backend = default_backend()
			)

		combinedKey = privateKey.decrypt(
			RSACipher,
			apadding.OAEP(
				mgf = apadding.MGF1(algorithm = hashes.SHA256()),
				algorithm = hashes.SHA256(),
				label = None
			)
		)

		# Split concatenated keys
		EncKey = combinedKey[:constants.KEY_LENGTH]
		HMACKey = combinedKey[constants.KEY_LENGTH:]

		# Call File Decryption
		MyFileDecryptMAC(fileName, cipherText, IV, tag, EncKey, HMACKey, ext)

		# Remove old json file
		jsonFile.close()
		os.remove(filePath)
