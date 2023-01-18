from picachu.domain.association_tables.association_tables import photo_object_table, \
    photo_emotion_table, photo_association_table
from picachu.domain.dal import db


class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    hash = db.Column(db.String(2048), nullable=True)
    photo_file_path_s3 = db.Column(db.String(2048), nullable=False)

    color = db.relationship('PhotoColor', back_populates="photo")

    objects = db.relationship(
        'Object', secondary=photo_object_table, back_populates='photos')

    emotions = db.relationship(
        'Emotion', secondary=photo_emotion_table, back_populates='photos')

    associations = db.relationship(
        'Association', secondary=photo_association_table, back_populates='photos')


    def __repr__(self):
        return f'<Photo {self.id!r} hash: {self.hash!r} s3_path:{self.photo_file_path_s3!r}>'
