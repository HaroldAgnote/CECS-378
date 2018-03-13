import os
import constants
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
	plainTextBytes = unpadder.update(paddedMessage) + unpadder.finalize()

	# Decode the bytes into a string
	plainText = plainTextBytes.decode("utf-8")

	# Return plain-text
	return plainText