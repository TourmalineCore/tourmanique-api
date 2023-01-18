import logging
from picachu.domain import Emotion, Association
from picachu.modules.labels.associations.commands.new_photo_association_command import NewPhotoAssociationCommand
from picachu.modules.labels.emotions.commands.new_photo_emotion_command import NewPhotoEmotionCommand
from picachu.domain import Object
from picachu.modules.labels.objects.commands.new_photo_object_command import NewPhotoObjectCommand
from picachu.domain import PhotoColor
from picachu.modules.labels.colors.commands.new_photo_color_command import NewPhotoColorCommand

insert_to_db_commands = {
    'emotion': NewPhotoEmotionCommand,
    'objects': NewPhotoObjectCommand,
    'colors': NewPhotoColorCommand,
    'association': NewPhotoAssociationCommand,
}

map_to_model_result = {
    'emotion': Emotion,
    'objects': Object,
    'colors': PhotoColor,
    'association': Association,
}


class AppendResultsCommand:
    @staticmethod
    def execute(result_message):
        logging.warning(f'Add result to db for message: {result_message}')
        for result in result_message['result']:
            try:
                result_to_entity = map_to_model_result[result_message['model_type']]
                result_entity = result_to_entity(**dict(result))
                print(result_entity)

                insert_to_db_command = insert_to_db_commands[result_message['model_type']]
                insert_to_db_command().create(result_entity, result_message['photo_id'])
                logging.warning('Results inserted.')

            except Exception as e:
                logging.error('Something went wrong! ' + str(e))
