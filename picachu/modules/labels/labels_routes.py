from flask import Blueprint

from picachu.modules.labels.associations.queries.get_association_query import GetAssociationQuery
from picachu.modules.labels.emotions.queries.get_emotions_query import GetEmotionQuery
from picachu.modules.labels.objects.queries.get_objects_query import GetObjectQuery
from picachu.modules.labels.colors.queries.get_colors_query import GetColorQuery
from picachu.modules.photos.queries.get_photos_query import GetPhotoQuery

import time

labels_blueprint = Blueprint('labels', __name__, url_prefix='/labels')


@labels_blueprint.route('/<photo_s3_path>', methods=['GET'])
def get_labels_by_photo_id(photo_s3_path: str):

    while True:
        photo = GetPhotoQuery().by_s3_path(photo_s3_path)
        if photo is None:
            continue
        photo_id = photo.id
        photo_hash = photo.hash
        break

    while True:
        emotions_response = GetEmotionQuery().by_photo_id(photo_id)
        if emotions_response is None:
            continue
        emotions_response = GetEmotionQuery().by_photo_id(photo_id).name
        break

    while True:
        objects_response = GetObjectQuery().by_photo_id(photo_id)
        if not objects_response:
            continue
        time.sleep(5)
        objects_response = [object_.name for object_ in GetObjectQuery().by_photo_id(photo_id)]
        break

    while True:
        color_response = GetColorQuery().by_photo_id(photo_id)
        if not color_response:
            continue
        color_response = list(map(lambda color: {"red": color.red, "green": color.green, "blue": color.blue},
                          GetColorQuery().by_photo_id(photo_id)))
        break

    while True:
        associations_response = GetAssociationQuery().by_photo_id(photo_id)
        if not associations_response:
            continue
        associations_response = [association.name for association in GetAssociationQuery().by_photo_id(photo_id)]
        break

    return {
        'hash': photo_hash,
        'objects': objects_response,
        'emotions': emotions_response,
        'photo_color': color_response,
        'associations': associations_response,
    }


@labels_blueprint.route('/', methods=['GET'])
def get_photo_with_model_results_but_without_associations():
    photos_with_model_results_but_without_associations = GetPhotoQuery().without_associative_tags()

    photo_ids = list(map(lambda photo: photo.id, photos_with_model_results_but_without_associations))
    print(photo_ids)
    response = []

    for photo_id in photo_ids:
        tags = []
        tags.extend([object_.name for object_ in GetObjectQuery().by_photo_id(photo_id)])
        tags.append(GetEmotionQuery().by_photo_id(photo_id).name)

        response.append({
            "photo_id": photo_id,
            "tags": tags
        })

    return response
