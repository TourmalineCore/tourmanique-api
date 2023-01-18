import imagehash
import io
import PIL.Image as Image
from picachu.helpers.s3_helper import S3Helper
from picachu.domain import Photo
from picachu.modules.photos.commands.new_photo_command import NewPhotoCommand


class ProcessPhotoRequestCommand:
    def __init__(self, session):
        self.session = session

    def execute(self, path_to_image_in_s3):
        photo_entity = Photo()
        photo_entity.photo_file_path_s3 = path_to_image_in_s3

        photo_bytes = S3Helper().s3_download_file(file_path_in_bucket=f'/{path_to_image_in_s3}')
        image = Image.open(io.BytesIO(photo_bytes))
        photo_entity.hash = str(imagehash.average_hash(image))

        return NewPhotoCommand(self.session).create_photo_without_commit(photo_entity)
