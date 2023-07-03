import numpy as np
from PIL import Image
from cryptography.fernet import Fernet

def encrypt_text(text, key):
    f = Fernet(key)
    encrypted_text = f.encrypt(text.encode())
    return encrypted_text

def encrypt_image(img_path: str, message: str, new_path: str):
    # Open the source image
    img = Image.open(img_path, 'r')
    # Get the dimensions of the image
    width, height = img.size
    # Convert image data into a numpy array
    array = np.array(list(img.getdata()))
    # Check the mode of the image
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    # Calculate the total number of pixels in the image
    total_pixels = array.size // n

    # Generate a Fernet key using the `generate_key()` method from the `Fernet` class
    key = Fernet.generate_key()

    # Encrypt the message using the `encrypt_text()` function and the generated key
    message = encrypt_text(message, key).decode('utf-8')
    
    # Append end of message string to the message
    message += "$end/REC"

    # Convert message characters into binary format
    b_message = ''.join([format(ord(i), "08b") for i in message])

    # Calculate the required number of pixels to hide the message
    req_pixels = len(b_message)

    # Check if the image has enough pixels to hide the message
    if req_pixels > total_pixels:
        raise ValueError("ERROR: Need larger file size")
    else:
        # Loop over each pixel in the image and modify it to hide the message bits
        index = 0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1
        # Reshape the numpy array back into an image format
        array = array.reshape(height, width, n)
        
        # Create a new image from the modified numpy array and save it to destination
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(new_path)
        print("Image Encoded Successfully")
    return key[:-1]


def decrypt_text(encrypted_text, key):
    f = Fernet(key)
    decrypted_text = f.decrypt(encrypted_text).decode()
    return decrypted_text

def decrypt_image(img_path, key):
    # Open the image to be decrypted
    img = Image.open(img_path, 'r')
    # Convert the image data into a numpy array
    array = np.array(list(img.getdata()))
    # Check the mode of the image
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    # Calculate the total number of pixels in the image
    total_pixels = array.size // n
    
    # Loop over each pixel in the image and extract the hidden bits
    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])
    # Split the extracted bits into groups of 8 to get the message characters
    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]
    # Convert the message characters from binary to ASCII characters
    message = ""
    for i in range(len(hidden_bits)):
        if message[-8:] == "$end/REC":
            break
        else:
            message += chr(int(hidden_bits[i], 2))

    # Check if the end of message string was found
    if "$end/REC" in message:
        return decrypt_text(bytes(message[:-8], 'utf-8'), key+'=')
    else:
        return None



# import gzip
# from PIL import Image
# from cryptography.fernet import Fernet
# import numpy  as np

# def encrypt_text(text, key):
#     f = Fernet(key)
#     encrypted_text = f.encrypt(text.encode())
#     return encrypted_text

# def check_palette(img):
#     """
#     Check if the image is in palette format, and convert it to full-color format if so.
#     """
#     if 'palette' in img.info:
#         img = img.convert('RGBA')
#         return img.convert('RGB')
#     return img.convert('RGB')

# def encrypt_image(img_path: str, message: str, new_path: str):
#     # Open the cover image and check its format
#     cover_image = Image.open(img_path)
#     cover_image = check_palette(cover_image)

#     compressed_data = gzip.compress(message.encode('utf-8'))
    
#     # Generate a new encryption key using Fernet
#     key = Fernet.generate_key()

#     # Create a Fernet object with the key
#     fernet = Fernet(key)

#     # Encrypt the hidden image using the Fernet object
#     encrypted_data = fernet.encrypt(compressed_data).decode('utf-8')

#     # Append end of message string to the message
#     encrypted_data += "$end/REC"

#     # Convert the encrypted data to binary format for embedding
#     binary_data = ''.join(format(x, '08b') for x in encrypted_data.encode('utf-8'))

#     fs = open("etest.txt", "w")
#     for i in str(binary_data):
#         fs.write(i)

#     # Embed the binary data within the cover image
#     pixels = cover_image.load()
#     width, height = cover_image.size
#     data_index = 0

#     for y in range(height):
#         for x in range(width):
#             # Get the RGB values of the current pixel
#             r, g, b = pixels[x, y]

#             # If there is more data to embed, modify the red value of the pixel
#             if data_index < len(binary_data):
#                 r = (r & 0xFE) | int(binary_data[data_index])
#                 data_index += 1

#             # If there is more data to embed, modify the green value of the pixel
#             if data_index < len(binary_data):
#                 g = (g & 0xFE) | int(binary_data[data_index])
#                 data_index += 1

#             # If there is more data to embed, modify the blue value of the pixel
#             if data_index < len(binary_data):
#                 b = (b & 0xFE) | int(binary_data[data_index])
#                 data_index += 1

#             # Set the modified pixel values
#             pixels[x, y] = (r, g, b)

#         # If there is no more data to embed, exit the loop
#         if data_index >= len(binary_data):
#             break
        
#         # Save the modified cover image
#         cover_image.save(new_path)
#         return key

# key = encrypt_image(r"C:\Users\Tushar Kumar\Desktop\steno\sunflower.png", "The quick brown fox jumps over the lazy dog", "stego_text.png")

# def decrypt_text(encrypted_text, key):
#     f = Fernet(key)
#     decrypted_text = f.decrypt(encrypted_text).decode()
#     return decrypted_text

# def decrypt_image(img_path, key):
#     # Open the image to be decrypted
#     img = Image.open(img_path, 'r')
#     # Convert the image data into a numpy array
#     array = np.array(list(img.getdata()))
#     # Check the mode of the image
#     if img.mode == 'RGB':
#         n = 3
#     elif img.mode == 'RGBA':
#         n = 4
#     # Calculate the total number of pixels in the image
#     total_pixels = array.size // n
    
#     # Loop over each pixel in the image and extract the hidden bits
#     hidden_bits = ""
#     for p in range(total_pixels):
#         for q in range(0, 3):
#             hidden_bits += (bin(array[p][q])[2:][-1])
#     # Split the extracted bits into groups of 8 to get the message characters
#     hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]
#     # Convert the message characters from binary to ASCII characters
    
#     fs = open("dtest.txt", "w")
#     for i in str("".join(hidden_bits)):
#         fs.write(i)

#     message = ""
#     for i in range(len(hidden_bits)):
#         if message[-8:] == "$end/REC":
#             break
#         else:
#             message += chr(int(hidden_bits[i], 2))

#     # Check if the end of message string was found

#     if "$end/REC" in message:
#         print("Hi")
#         return decrypt_text(bytes(message[:-8], 'utf-8'), key+'=')
#     else:
#         return None

# print(decrypt_image('stego_text.png', key.decode()))