from picachu.domain import Object, photo_object_table
from picachu.domain.dal import create_session
from picachu.modules.labels.objects.commands.new_objects_command import NewObjectCommand
from picachu.modules.labels.objects.queries.get_objects_query import GetObjectQuery



class NewPhotoObjectCommand:
    def __init__(self):
        pass

    @staticmethod
    def create(object_entity: Object, photo_id: int) -> int:
        current_session = create_session()

        object = GetObjectQuery().by_name(object_entity.name)

        if not object:
            object_id = NewObjectCommand().create(object_entity)
        else:
            object_id = object.id

        try:
            statement = photo_object_table.insert().values(photo_id=photo_id,
                                                           object_id=object_id)
            current_session.execute(statement)
            current_session.commit()

        finally:
            current_session.close()
