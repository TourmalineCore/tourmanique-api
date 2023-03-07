from picachu.domain.data_access_layer.db import db


class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    hash = db.Column(db.String(2048), nullable=True)
    photo_file_path_s3 = db.Column(db.String(2048), nullable=False)

    def __repr__(self):
        return f'<Photo {self.id!r} hash: {self.hash!r} s3_path:{self.photo_file_path_s3!r}>'
