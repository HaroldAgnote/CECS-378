import constants
filePath = ".publicKey.pem"
print(not (filePath.endswith(constants.PRIVATE_KEY_FILE_PATH) or filePath.endswith(constants.PUBLIC_KEY_FILE_PATH) or filePath.endswith(constants.PAYLOAD_FILE_PATH)))