from internal.application.hill_cipher.service import Service as HillService
from internal.application.images.util import convert_to_byte_array
from internal.ports.images.storage import ImageStorage

BLOCK_SIZE = 3


class Service:

    def __init__(self, storage: ImageStorage):
        self.__storage = storage


    def encrypt(self, dir: str = None):
        input_image = self.__storage.compute(dir)

        cipher = HillService()

        key, padded_image = cipher.generate_key(input_image, BLOCK_SIZE)        
        encrypted = cipher.encrypt(key, padded_image, BLOCK_SIZE)

        key_bytes = convert_to_byte_array(key, 'tiff')
        encrypted_bytes = convert_to_byte_array(encrypted, 'tiff')

        self.__storage.save_key(key_bytes, dir)
        self.__storage.save_encrypted(encrypted_bytes, dir)