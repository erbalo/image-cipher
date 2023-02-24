import numpy as np

from PIL import Image
from typing import Tuple
from sympy import Matrix
from internal.application.images.util import multiply, pad


class Service:

    def __generate_sub_key(self, n):
        '''
        Generate an nxn matrix that is invertible mod 256
        Args:
            n (int): The size of the matrix
        Returns:
            ndarray: nxn array modularly invertible 256
        '''
        found = False
        while(not found):
            key = np.array([[np.random.randint(256)
                    for _ in range(0, n)] for _ in range(0, n)], dtype="uint8")
            try:
                Matrix(key).inv_mod(256)
                found = True
            except:
                pass

        return key


    def generate_key(self, image: Image.Image, block_size) -> Tuple:
        '''
        Generate an mxn matrix that consists of 3x3 keys (invertible mod 256).
            This is the key to encode the image with
        Args:
            width (int): width of the key Image to generate
            height (int): height of the key Image to generate
            block_size (int): size of the square subkey that will be tiled to form the key image
        Returns:
            PIL.Image: The tiled key as an image 
        '''
        image_pixels = np.array(image)

        padded_image = pad(image_pixels, block_size)
        image_pixels = np.array(padded_image)

        width = len(image_pixels)
        height = len(image_pixels[0])

        key = np.empty((width, height), dtype='uint8')
        sub_key = self.__generate_sub_key(block_size)
        i = j = 0

        while i < width:
            while j < height:
                key[i:i + block_size, j:j + block_size] = sub_key
                j += block_size
            i += block_size
            j = 0

        key = Image.fromarray(key)
        
        return Image.merge('RGB', (key, key, key)), padded_image


    def invert_key(self, key, block_size):
        '''
        Convert a key to the inverse mod 256 for decrypting
        Args:
            key (PIL.Image): The key image to invert
            block_size (int): The size of the keys tiled in the key image (nxn Square key, block_size = n)
            complexKey (bool): Was the key generatedusing the -c flag (non-uniform tiled key)
        Returns:
            PIL.Image: the inverse key as an image
        '''
        i = j = 0

        key = np.array(key.split()[0])
        sub_key = np.array(Matrix(key[i:i + block_size, j:j + block_size]).inv_mod(256))

        while i < len(key):
            while j < len(key[0]):
                key[i:i + block_size, j:j + block_size] = sub_key
                j += block_size
            i += block_size
            j = 0

        key = Image.fromarray(np.uint8(key))

        return Image.merge('RGB', (key, key, key))


    def encrypt(self, key, image, block_size):
        '''
        Encodes an image with a given key
        Args:
            key (PIL.Image): The key to use for encryption
            image (PIL.Image): The image to encrypt
            block_size (int): The size of the square keys to be tiled 
        Returns:
            PIL.Image: The encrypted image
        '''
        multiplied = multiply(key, image, block_size)
        multiplied = np.array(multiplied)

        return Image.fromarray(np.uint8(np.mod(multiplied, 256)))


    def decrypt(self, key, image, block_size):
        '''
        Decodes an image with a given key
        Args:
            key (PIL.Image): The key used to encrypt the image
            image (PIL.Image): Image to decrypt
            block_size (int): size of the subkey tiled to form the key image
            complexKey (bool): Was the image encrypted with the -c flag?
        Returns:
            PIL.Image: Decrypted Image
        '''
        return self.encrypt(self.invert_key(key, block_size), image, block_size)