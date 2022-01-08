import cv2
import tensorflow as tf
import imutils
import numpy as np

from .mlmodel import answer, crop_image, predict_sbd_md

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
    img = cv2.imread("/home/covid19/github/chamdiem" + str(imgurl))
    predict_c = predict_sbd_md()
    crop_sbd = predict_c.crop_image_sbd(img)
    crop_md = predict_c.crop_image_md(img)  
    split_sbd = predict_c.split_blocks_sbd(crop_sbd)
    split_md = predict_c.split_blocks_md(crop_md)
    list_answer_sbd = predict_c.list_ans(split_sbd) 
    list_answer_md = predict_c.list_ans(split_md) 
    return predict_c.get_answers(list_answer_sbd), predict_c.get_answers(list_answer_md)