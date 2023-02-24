import abc

from PIL import Image


class ImageStorage(abc.ABC):

    def __init__(self, file_name: str, extension: str):
        self._file_name = file_name
        self._extension = extension
        self._full_file_name = f'{self._file_name}.{self._extension}'
        self._key_name = f'{self._file_name}-key.tiff'
        self._encrypted_name = f'{self._file_name}-encrypted.tiff'


    @abc.abstractmethod
    def compute(self, dir: str = None) -> Image.Image:
        pass


    @abc.abstractmethod
    def save_key(self, image_bytes: bytes, dir: str = None):
        pass


    @abc.abstractmethod
    def save_encrypted(self, image_bytes: bytes, dir: str = None):
        pass
