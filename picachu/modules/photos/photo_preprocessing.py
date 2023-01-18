import cv2
import numpy as np


def preprocess_photo(photo):
    if photo.mode != "RGB":
        photo = np.array(photo.convert('RGB'))
    else:
        photo = np.array(photo)

    modified_photo = cv2.resize(photo,
                                (600, 400),
                                interpolation=cv2.INTER_AREA)
    modified_photo = modified_photo.reshape(modified_photo.shape[0] * modified_photo.shape[1],
                                            3)
    return modified_photo
