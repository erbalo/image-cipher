
import io

from PIL import Image
from internal.ports.images.storage import ImageStorage


class MachineStore(ImageStorage):

    def __init__(self, file_name: str, extension:str):
        super().__init__(file_name, extension)


    def compute(self) -> Image.Image:
        file_name = self._full_file_name
        return Image.open(file_name)


    def save_key(self, image_bytes: bytes, dir: str = None):
        key_mem = Image.open(io.BytesIO(image_bytes))
        key_mem.save(self._key_name)


    def save_encrypted(self, image_bytes: bytes, dir: str = None):
        encrypted_mem = Image.open(io.BytesIO(image_bytes))
        encrypted_mem.save(self._encrypted_name)