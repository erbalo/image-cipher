import io

from PIL import Image
from internal.ports.images.storage import ImageStorage
from internal.adapters.aws.client import S3


class S3Storage(ImageStorage):
    
    def __init__(self, file_name: str, extension: str, s3_client: S3):
        super().__init__(file_name, extension)
        self.__s3_client = s3_client


    def compute(self, dir: str = None) -> Image.Image:
        image_bytes = self.__s3_client.get_object(dir, self._full_file_name)
        return Image.open(io.BytesIO(image_bytes))


    def save_key(self, image_bytes: bytes, dir: str = None):
        self.__s3_client.upload_object(image_bytes, dir, self._key_name)


    def save_encrypted(self, image_bytes: bytes, dir: str = None):
        self.__s3_client.upload_object(image_bytes, dir, self._encrypted_name)
