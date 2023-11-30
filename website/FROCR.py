# !pip install tesseract
# !pip install pytesseract
import tensorflow as tf
import numpy as np
from PIL import Image

from keras import backend as K
import os

K.set_image_data_format('channels_last')
from .inception_resnet_v1 import *
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

model = InceptionResNetV1(weights_path='keras-facenet-h5/model.h5')
FRmodel = model


def img_to_encoding(image_path):
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(160, 160))
    img = np.around(np.array(img) / 255.0, decimals=12)
    x_train = np.expand_dims(img, axis=0)
    embedding = FRmodel.predict_on_batch(x_train)
    return embedding / np.linalg.norm(embedding, ord=2)


def OCR(image_path):
    img = Image.open(image_path)
    extractedInformation = pytesseract.image_to_string(img, )
    try:
        index1 = extractedInformation.find("First name:")
        lit1 = extractedInformation[index1 + 12:].split('\n')
        first_name = lit1[0].upper()
    except:
        return False, False

    try:
        index2 = extractedInformation.find("Last name:")
        lit2 = extractedInformation[index2 + 11:].split('\n')
        last_name = lit2[0].upper()
    except:
        return False, False

    return first_name, last_name


def FV_check(image_path, identity):

    p = os.path.sep.join(['shots', identity + "_img.jpg"])
    orginal_img = img_to_encoding(p)
    encoding = img_to_encoding(image_path)

    dist = np.linalg.norm(encoding - orginal_img)
    print("dist is :", dist)
    if dist < 0.7:
        return True
    else:
        return False
