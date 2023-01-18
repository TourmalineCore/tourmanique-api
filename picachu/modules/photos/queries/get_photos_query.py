from picachu.domain import Photo, photo_emotion_table, PhotoColor, photo_object_table
from picachu.domain.association_tables.association_tables import photo_association_table
from picachu.domain.dal import create_session


class GetPhotoQuery:

    def __init__(self):
        pass

    def by_id(self, photo_id):
        current_session = create_session()
        try:
            return current_session \
                .query(Photo) \
                .filter(Photo.id == photo_id) \
                .one_or_none()

        finally:
            current_session.close()

    def by_s3_path(self, photo_path_in_s3):
        current_session = create_session()
        try:
            return current_session \
                .query(Photo) \
                .filter(Photo.photo_file_path_s3 == photo_path_in_s3) \
                .one_or_none()

        finally:
            current_session.close()

    def without_associative_tags(self):
        current_session = create_session()
        try:

            photos_with_model_tags = current_session \
                .query(Photo) \
                .join(PhotoColor) \
                .join(photo_emotion_table) \
                .join(photo_object_table) \
                .filter(Photo.id != None) \
                .group_by(Photo.id) \
                # .all()
            # .filter(PhotoColor.photo_id != None) \
            # .filter(photo_object_table.c.object_id != None) \
            # .filter(photo_association_table.c.association_id != None)

            photos_with_association_tags = current_session \
                .query(Photo) \
                .join(PhotoColor) \
                .join(photo_association_table) \
                .filter(Photo.id != None) \
                .group_by(Photo.id) \
                # .all()

            return photos_with_model_tags.except_(photos_with_association_tags).all()
            # return current_session\
            #     .query(Photo) \
            #     .join(PhotoColor) \
            #     .join(photo_emotion_table) \
            #     .join(photo_object_table) \
            #     .join(photo_association_table) \
            #     .filter(photo_emotion_table.c.emotion_id != None) \
            #     .filter(PhotoColor.photo_id !=  None) \
            #     .filter(photo_object_table.c.object_id !=  None) \
            #     .filter(photo_association_table.c.association_id != None) \
            #     .group_by(Photo.id) \
            #     .all()

        finally:
            current_session.close()
