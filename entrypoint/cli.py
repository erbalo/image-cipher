import sys

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PIL import Image
from internal.application.images.service import Service as ImageService
from internal.application.hill_cipher.service import Service as Hill
from internal.adapters.storage.machine.handler import MachineStore


if __name__ == '__main__':
    if len(sys.argv) > 1:
        image_file_name = sys.argv[1]
    else:
        raise Exception('Missing image file name')

    block_size = 3

    img_name = image_file_name.split('.')[0]
    img_extension = image_file_name.split('.')[1]

    storage = MachineStore(img_name, img_extension)
    service = ImageService(storage)

    service.encrypt()

    key_filename = f'{img_name}-key.tiff'
    encrypted_file_name = f'{img_name}-encrypted.tiff'

    key_image = Image.open(key_filename)
    encrypted_image = Image.open(encrypted_file_name)

    cipher = Hill()

    decrypted_file_name = f'{img_name}-decrypted.{img_extension}'
    decrypted = cipher.decrypt(key_image, encrypted_image, block_size)

    decrypted.save(decrypted_file_name)
