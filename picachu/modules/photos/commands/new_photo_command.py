from picachu.domain import Photo
from picachu.domain.dal import create_session
from picachu.requests_consumer.commands.send_model_request_command import SendModelRequestCommand


class NewPhotoCommand:

    def __init__(self, session):
        self.session = session

    def create_photo_without_commit(self, photo_entity: Photo) -> int:
        self.session.add(photo_entity)
        self.session.flush()
        self.session.refresh(photo_entity)

        send_model_request_command = SendModelRequestCommand(self.session.rollback)
        send_model_request_command.execute(
            photo_entity.id,
            photo_entity.photo_file_path_s3,
        )

        return photo_entity.id
