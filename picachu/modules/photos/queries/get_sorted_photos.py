from picachu.domain import Photo

class GetSortedQuery:
    @classmethod
    def sorted(cls, gallery_id) -> int:
query = Photo.query.filter(gallery_id=gallery_id).order_by(Photo.uniqueness.desc(), Photo.date_of_upload)
query = Photo.query.filter(gallery_id=gallery_id).order_by(Photo.date_of_upload.desc())
