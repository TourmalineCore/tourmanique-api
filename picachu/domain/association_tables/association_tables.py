from picachu.domain.dal import db

photo_object_table = db.Table(
    'photo_object',
    db.Column('photo_id', db.Integer(), db.ForeignKey('photos.id'), primary_key=True),
    db.Column('object_id', db.Integer(), db.ForeignKey('objects.id'), primary_key=True),
)

photo_emotion_table = db.Table(
    'photo_emotion',
    db.Column('photo_id', db.Integer(), db.ForeignKey('photos.id'), primary_key=True),
    db.Column('emotion_id', db.Integer(), db.ForeignKey('emotions.id'), primary_key=True),
)

photo_association_table = db.Table(
    'photo_association',
    db.Column('photo_id', db.Integer(), db.ForeignKey('photos.id'), primary_key=True),
    db.Column('association_id', db.Integer(), db.ForeignKey('associations.id'), primary_key=True),
)


