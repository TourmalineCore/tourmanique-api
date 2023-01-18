from picachu.domain.association_tables.association_tables import photo_association_table
from picachu.domain.dal import db


class Association(db.Model):
    __tablename__ = 'associations'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(2048), nullable=False)

    photos = db.relationship(
        'Photo', secondary=photo_association_table, back_populates='associations'
    )

    def __repr__(self):
        return f'<Association {self.id!r} name:{self.name!r}>'