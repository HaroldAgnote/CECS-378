import os
import base64
import constants
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as apadding
from cryptography.hazmat.primitives import padding, serialization, hashes, hmac
from cryptography.hazmat.backends import default_backend

def MyEncryptMAC(plainText, EncKey, HMACKey):
	# Verify that the key is 256-bits
	if len(EncKey) < constants.KEY_LENGTH:
		print("Key must be 256-bits")
		return None, None, None
	if	len(HMACKey) < constants.KEY_LENGTH:
		print("HMAC Key must be 256-bits")
		return None, None, None
	else:
		# Default backend
		backend = default_backend()

		# Generate a random IV
		IV = os.urandom(constants.IV_LENGTH)

		# Set up cipher with AES-CBC and the passed key and generated IV
		cipher = Cipher(algorithms.AES(EncKey), modes.CBC(IV), backend = backend)

		# Pad the message so it can work with CBC
		padder = padding.PKCS7(constants.CBC_BLOCK_LENGTH).padder()
		paddedPlainText = padder.update(plainText) + padder.finalize()

		# Encrypt the padded message
		encryptor = cipher.encryptor()
		cipherText = encryptor.update(paddedPlainText) + encryptor.finalize()

		# HMAC
		tag = hmac.HMAC(HMACKey, hashes.SHA256(), backend = backend)
		tag.update(cipherText)
		tag = tag.finalize()
		
		# Return the encrypted message and IV
		return cipherText, IV, tag

def MyFileEncryptMAC(filePath):
	# Verify filepath is a file
	if(not os.path.isfile(filePath)):
		print("File not found")
	else:
		# Generate random key and HMAC Key
		EncKey = os.urandom(constants.KEY_LENGTH)
		HMACKey = os.urandom(constants.KEY_LENGTH)

		# Split filePath into fileName and ext
		filename, ext = os.path.splitext(filePath)

		# Initialize data from file
		data = ""

		# Extract data from file
		with open(filePath, 'rb') as f:
				data = f.read()

		# Call the Encryption and MAC
		encryptedFile, IV, tag = MyEncryptMAC(data, EncKey, HMACKey)

		# Return the encrypted file, IV, tag, EncKey, HMACKey, and file extension
		return encryptedFile, IV, tag, EncKey, HMACKey, ext

def MyRSAEncryptMAC(filePath, RSAPublicKeyFilePath):
	# Verify RSA PublicKeyFilePath is a file
	if(not os.path.isfile(RSAPublicKeyFilePath)):
		print("RSA Public Key File not found")
	else:
	  	# Call the File Encryption and MAC
		encryptedFile, IV, tag, EncKey, HMACKey, ext = MyFileEncryptMAC(filePath)

		# Concatenate keys for RSA Encryption
		RSAKey = EncKey + HMACKey

		# Initialize the public key and read it from file for use in RSA
		public_key = ""
		with open(RSAPublicKeyFilePath, 'rb') as keyFile:
	  		public_key = serialization.load_pem_public_key(keyFile.read(), backend = default_backend())

		# Encrypt the concatenated keys with RSA
		RSACipher = public_key.encrypt(
			RSAKey, 
	  		apadding.OAEP(
	  			mgf = apadding.MGF1(algorithm = hashes.SHA256()), 
	  			algorithm = hashes.SHA256(), 
	  			label = None
	  		)
	  	)

		# Return the encrypted keys, encrypted file, IV, tag, and file extension
		return RSACipher, encryptedFile, IV, tag, ext