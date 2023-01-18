from picachu.domain.association_tables.association_tables import photo_object_table
from picachu.domain.dal import db


class Object(db.Model):
    __tablename__ = 'objects'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(2048), nullable=False)

    photos = db.relationship(
        'Photo', secondary=photo_object_table, back_populates='objects'
    )

    def __repr__(self):
        return f'<Object {self.id!r} name:{self.name!r}>'
