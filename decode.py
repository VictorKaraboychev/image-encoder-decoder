from PIL import Image
from itertools import product
    
def getBit(byte, offset):
    return int(byte & 2**offset != 0)

def appendBit(byte, bit):
    byte <<= 1
    return byte | bit

def decode(image):
    current_bit = 0
    current_byte = 0
    accumulated_byte = 0

    data_density = 0
    data_length = 0
    file_suffix = ''
    data = bytearray()

    for y, x in product(range(image.height), range(image.width)):
        image_data = image.getpixel((x, y))

        for c in range(4):
            for o in range(data_density, -1, -1):
                accumulated_byte = appendBit(accumulated_byte, getBit(image_data[c], o))

                current_bit = (current_bit + 1) % 8
                if current_bit % 8 == 0:
                    if (current_byte == 0): # reads data density 
                        data_density = accumulated_byte

                    if (current_byte > 0 and current_byte <= 8): # reads file length
                        data_length += accumulated_byte * 256**(7-(current_byte - 1))

                    if (current_byte > 8 and current_byte <= 16): # reads file suffix
                        if (accumulated_byte != 0):
                            file_suffix = chr(accumulated_byte) + file_suffix

                    if (current_byte > 16 and current_byte <= (data_length + 16)): # reads data
                        data.append(accumulated_byte)
                    
                    accumulated_byte = 0
                    current_byte += 1
        if (current_byte > (data_length + 16)): break
    return [data, file_suffix]