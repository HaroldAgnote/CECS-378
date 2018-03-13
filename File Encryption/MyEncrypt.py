import os
import constants
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def MyEncrypt(plainText, key):
	# Verify that the key is 256-bits
	if len(key) < constants.KEY_LENGTH:
		print("Key must be 256-bits")
	else:
		# Default backend
		backend = default_backend()

		# Generate a random IV
		IV = os.urandom(constants.IV_LENGTH)

		# Set up cipher with AES-CBC and the passed key and generated IV
		cipher = Cipher(algorithms.AES(key), modes.CBC(IV), backend = backend)

		# Convert the message into bytes
		plainTextBytes = bytes(message,'utf-8')

		# Pad the message so it can work with CBC
		padder = padding.PKCS7(constants.CBC_BLOCK_LENGTH).padder()
		paddedPlainTextBytes = padder.update(plainTextBytes) + padder.finalize()

		# Encrypt the padded message
		encryptor = cipher.encryptor()
		cipherText = encryptor.update(paddedPlainTextBytes) + encryptor.finalize()
		
		# Return the encrypted message and IV
		return cipherText, IV

def MyFileEncrypt(filePath):
	# Verify filepath is a file
	if(os.path.isfile(filePath)):
		print("File not found")
	else:
		# Generate random IV and key
		key = os.urnadom(constants.KEY_LENGTH)
		IV = os.urandom(constants.IV_LENGTH)

		#

		# Return the encrypted file, IV, key, and file extension
		return encryptedFile, IV, key, ext