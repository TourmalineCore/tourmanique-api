from sqlalchemy.orm import relationship

from picachu.domain.association_tables.association_tables import photo_emotion_table
from picachu.domain.dal import db


class Emotion(db.Model):
    __tablename__ = 'emotions'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(2048), nullable=False)

    photos = db.relationship(
        'Photo', secondary=photo_emotion_table, back_populates='emotions'
    )

    def __repr__(self):
        return f'<Emotion {self.id!r} name:{self.name!r}>'
