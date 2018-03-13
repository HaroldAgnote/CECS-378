import os
import MyEncrypt
import MyDecrypt
import constants

# Allows the user to input a message to encrypt/decrypt
print("Message Encryptor/Decryptor")
print("---------------------------")

# Get the user's input for the message to encrypt/decrypt
message = input("Enter a message to encrypt: ")

# Generate a key
key = os.urandom(constants.KEY_LENGTH)

# Call the encryptor
cipherText, IV = MyEncrypt.MyEncrypt(plainText = message,key = key)

# Display the results of encryption
print("---------------------")
print("Results of Encryption")
print("ciphertext: ", end="")
print(cipherText)
print("IV: ", end="")
print(IV)

# Decrypt the encrypted message
decryptedMessage = MyDecrypt.MyDecrypt(cipherText = cipherText, key = key, IV = IV)

# Display the results of decryption
print("---------------------")
print("Results of Decryption")
print("plaintext: ", end="")
print(decryptedMessage)

# Allows the user to input a filepath of a file to encrypt/decrypt
print("File Encryptor/Decryptor")
print("---------------------------")

# Get the user's input for the filepath of a file to encrypt/decrypt
# Use larry.png as sample
filePath = input("Enter the filepath of a file to encrypt: ")

# Call the encryptor
cipherText, IV, key, ext = MyEncrypt.MyFileEncrypt(filePath = filePath)

# Display the results of encryption
print("---------------------")
print("Results of Encryption")
print("cipherText: ", end="")
print(cipherText)
print("IV: ", end="")
print(IV)
print("key: ", end="")
print(key)
print("extension: ", end="")
print(ext)

# Decrypt the encrypted message
decryptedFile = MyDecrypt.MyFileDecrypt(cipherText = cipherText, key = key, IV = IV, ext = ext)

# Display the results of decryption
print("---------------------")
print("Results of Decryption")
print("file: ", end="")
print(decryptedFile)


os.system("pause")