import cv2
import tensorflow as tf
import imutils
import numpy as np

from .mlmodel import answer, crop_image

def result(imgurl='/media/uploads/1_Ca0WIXe.jpg'):
    
    img = cv2.imread("/home/covid19/github/chamdiem" + str(imgurl))
    img = cv2.resize(img, (1000,1500))
    model = tf.keras.models.load_model('weight11.h5')
    crop = answer()
    ans_blocks = crop.crop_image(img)
    list_answer = crop.divide_ans_blocks(ans_blocks)
    list_answer = crop.list_ans(list_answer)
    return crop.get_answers(list_answer, model)

def predict(img, model):
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_gray = cv2.GaussianBlur(img_gray,(3,3),0)
    ret, im_th = cv2.threshold(img_gray, 179, 255, cv2.THRESH_BINARY_INV)
    roi = cv2.resize(im_th,(28,28),interpolation=cv2.INTER_AREA)
    roi = roi / 255.0
    y = model.predict(roi.reshape(-1,28,28,1))
    return np.argmax(y)

def get_sbd(imgurl='/media/uploads/1_Ca0WIXe.jpg'):
    model = tf.keras.models.load_model('weight_18_12.h5')
    img = cv2.imread('/home/covid19/github/chamdiem' + str(imgurl))
    img = cv2.resize(img, (1100,1500))

    crop = crop_image()

    # SBD
    a = crop.crop_image_sbd(img)
    b = crop.split_blocks_sbd(a)

    # MaDe
    a1 = crop.crop_image_md(img)
    b1 = crop.split_blocks_md(a1)

    sbd = ''
    for i in range(len(b)):
        y = predict(b[i], model)
        sbd += str(y)

    md = ''
    for i in range(len(b1)):
        y = predict(b1[i], model)
        md += str(y)

    return sbd, md