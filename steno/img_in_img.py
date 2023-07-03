import base64
from PIL import Image
from io import BytesIO
from cryptography.fernet import Fernet
import gzip
import os

def check_palette(img):
    """
    Check if the image is in palette format, and convert it to full-color format if so.
    """
    if 'palette' in img.info:
        img = img.convert('RGBA')
        return img.convert('RGB')
    return img.convert('RGB')

def encrypt_image(cover_image: str, hidden_image: str, output_path: str) -> str :
    print(os.path.getsize(hidden_image))

    """
    Function to encode a hidden image within a cover image and return the encryption key and metadata.
    Args:
        cover_image (str): Path to the cover image.
        hidden_image (str): Path to the image to be hidden.
    Returns:
        str: Encryption key and metadata as a string.
    """
    # Open the cover image and check its format
    cover_image = Image.open(cover_image)
    cover_image = check_palette(cover_image)
    
    # Open the image to be hidden and check its format
    hidden_image = Image.open(hidden_image)
    hidden_image = check_palette(hidden_image)

    if cover_image.size[0] >= hidden_image.size[0] and cover_image.size[1] >= hidden_image.size[1]:
        
        # Compress and encrypt the hidden image
        buffer = BytesIO()

        # Compress the hidden image using gzip
        with gzip.GzipFile(fileobj=buffer, mode="wb") as f:
            compressed_data = hidden_image.tobytes('raw', 'RGB')
            f.write(compressed_data)
            
        # Move the buffer's position to the start
        buffer.seek(0)

        # Generate a new encryption key using Fernet
        key = Fernet.generate_key()

        # Create a Fernet object with the key
        fernet = Fernet(key)

        # Encrypt the hidden image using the Fernet object
        encrypted_data = fernet.encrypt(buffer.read())

        # Write the encrypted data to a file for logging purposes
        with open('elog.txt', 'wb') as f:
            f.write(encrypted_data)
        
        # Convert the encrypted data to binary format for embedding
        binary_data = ''.join(format(x, '08b') for x in encrypted_data)

        # Embed the binary data within the cover image
        pixels = cover_image.load()
        width, height = cover_image.size
        data_index = 0

        for y in range(height):
            for x in range(width):
                # Get the RGB values of the current pixel
                r, g, b = pixels[x, y]

                # If there is more data to embed, modify the red value of the pixel
                if data_index < len(binary_data):
                    r = (r & 0xFE) | int(binary_data[data_index])
                    data_index += 1

                # If there is more data to embed, modify the green value of the pixel
                if data_index < len(binary_data):
                    g = (g & 0xFE) | int(binary_data[data_index])
                    data_index += 1

                # If there is more data to embed, modify the blue value of the pixel
                if data_index < len(binary_data):
                    b = (b & 0xFE) | int(binary_data[data_index])
                    data_index += 1

                # Set the modified pixel values
                pixels[x, y] = (r, g, b)

            # If there is no more data to embed, exit the loop
            if data_index >= len(binary_data):
                break

        # Save the modified cover image
        cover_image.save(output_path)

        # Save some metadata of an hidden image (encrypted byte length & hidden image size)
        hidden_image_size = "".join(str(hidden_image.size).split(" "))[1:-1]
        hidden_image_size = base64.b64encode(hidden_image_size.encode('utf-8'))
        hidden_encrypted_byte_size = base64.b64encode(str(len(encrypted_data))\
                                           .encode('utf-8'))\
                                           .decode('utf-8')

        # Return the encryption key and metadata as a string
        return (key[:-1] + hidden_image_size).decode('utf-8')\
                                             .rstrip('=')+'@'+hidden_encrypted_byte_size
    raise ValueError("Error: The cover image dimensions are not large enough to hide the hidden image. The cover image must be at least as large as the hidden image in both width and height.\nPlease resize the cover image to meet the minimum size requirement or choose a different cover image.")

def decrypt_image(image, _key, output_path):
    # Open the embedded image
    embedded_image = Image.open(image)
    # Convert the image to RGB format
    embedded_image = embedded_image.convert("RGB")
    # Extract the encrypted data from the image
    pixels = embedded_image.load()
    width, height = embedded_image.size
    binary_data = ""
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    # Convert the binary data to bytes
    byte_list = []
    for i in range(0, len(binary_data), 8):
        temp = int(binary_data[i:i+8], 2)
        byte_list.append(temp)

    encrypted_data = bytes(byte_list)

    # Write the encrypted data to a file for logging purposes
    with open('dlog.txt', 'wb') as f:
            f.write(encrypted_data)

    image_size_base64 = _key[43:].split('@')[0]
    image_size = base64.b64decode(image_size_base64 + '='*(len(image_size_base64) % 4))\
                       .decode('utf-8')
    image_size = tuple(map(int, image_size.split(',')))

    encrypted_len = int(base64.b64decode(_key.split('@')[-1])
                              .decode('utf-8'))
    encrypted_data = str(encrypted_data)[2:encrypted_len+2]
    
    # Decrypt and decompress the data
    byte_key = bytes(_key[:43]+'=', 'utf-8')
    fernet = Fernet(byte_key)
    decrypted_data = fernet.decrypt(encrypted_data)

    buffer = BytesIO(decrypted_data)
    with gzip.GzipFile(fileobj=buffer, mode="rb") as f:
        hidden_image = Image.frombytes("RGB", image_size, f.read())
    # Save the hidden image
    hidden_image.save(output_path)