
import tensorflow as tf

import imutils
import numpy as np
import cv2
from math import ceil
from collections import defaultdict
import matplotlib.pyplot as plt

class answer:
    def get_x_ver1(self,s):
        s = cv2.boundingRect(s)
        return s[0] * s[1]

    def get_x(self,s):
          return s[1][0]
          
    def pre_processing_img(self,img):
       # convert image from BGR to GRAY to apply canny edge detection algorithm
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # remove noise by blur image
        blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)

        # apply canny edge detection algorithm
        img_canny = cv2.Canny(blurred, 100, 200)

        # find contours
        cnts = cv2.findContours(img_canny.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        return cnts,gray_img

    def crop_image(self,img):
        cnts,gray_img = self.pre_processing_img(img)

        ans_blocks = []
        x_old, y_old, w_old, h_old = 0, 0, 0, 0

        # ensure that at least one contour was found
        if len(cnts) > 0:
            # sort the contours according to their size in descending order
            cnts = sorted(cnts, key=self.get_x_ver1)

            # loop over the sorted contours
            for i, c in enumerate(cnts):
                x_curr, y_curr, w_curr, h_curr = cv2.boundingRect(c)

                if w_curr * h_curr > 100000 and w_curr < h_curr:
                    # check overlap contours
                    check_xy_min = x_curr * y_curr - x_old * y_old
                    check_xy_max = (x_curr + w_curr) * (y_curr + h_curr) - (x_old + w_old) * (y_old + h_old)

                    # if list answer box is empty
                    if len(ans_blocks) == 0:
                        ans_blocks.append(
                            (gray_img[y_curr:y_curr + h_curr, x_curr:x_curr + w_curr],[x_curr,y_curr,w_curr,h_curr]))
                        # update coordinates (x, y) and (height, width) of added contours
                        x_old,y_old,w_old,h_old = x_curr,y_curr,w_curr,h_curr

                    elif check_xy_min > 20000 and check_xy_max > 20000:
                        ans_blocks.append(
                            (gray_img[y_curr:y_curr + h_curr, x_curr:x_curr + w_curr],[x_curr,y_curr,w_curr,h_curr]))
                        # update coordinates (x, y) and (height, width) of added contours
                        x_old,y_old,w_old,h_old = x_curr,y_curr,w_curr,h_curr

            # sort ans_blocks according to x coordinate
            sorted_ans_blocks = sorted(ans_blocks, key=self.get_x)
            return sorted_ans_blocks

    def divide_ans_blocks(self,ans_blocks):
        """
          Mỗi blocks đáp án có 6 ô nhỏ mỗi ô nhỏ sẽ có 5 câu 
          Do 4 blocks có độ dài bằng nhau sẽ chia ra 6 ô nhỏ 

          """
        list_answers = []
        for ans_block in ans_blocks:
            ans_block_img = np.array(ans_block[0])
            offset1 = ceil(ans_block_img.shape[0] / 6)
            for i in range(6):
                    box_img = np.array(ans_block_img[i * offset1:(i + 1) * offset1, :])
                    height_box = box_img.shape[0]
                    box_img = box_img[14:height_box-14, :]
                    offset2 = ceil(box_img.shape[0] / 5)
                    for j in range(5):
                          list_answers.append(box_img[j * offset2:(j + 1) * offset2, :])
        return list_answers

    def list_ans(self,list_answers):
        """
            - có 120 câu thì sẽ có 4 đáp án thì tổng sẽ có 120 * 4 = 480
            - Để crop mỗi lựa chọn thì lặp qua 4 rồi chọn khoảng crop ra (start lấy tự vị trí đầu cho mỗi đáp án bỏ qua số thứ tự và offset là ví trị kq dừng)

          """
        list_choices = []
        for answer_img in list_answers:
            start = 40
            offset = 40
            for i in range(4):
                    bubble_choice = answer_img[:,start + i * offset:start + (i + 1) * offset]
                    bubble_choice = cv2.threshold(bubble_choice, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                    bubble_choice = cv2.resize(bubble_choice, (28, 28), cv2.INTER_AREA)
                    bubble_choice = bubble_choice.reshape((28, 28, 1))
                    list_choices.append(bubble_choice)
        return list_choices

    def map_answer(self,idx):
        if idx % 4 == 0:
            answer_circle = "A"
        elif idx % 4 == 1:
            answer_circle = "B"
        elif idx % 4 == 2:
            answer_circle = "C"
        else:
            answer_circle = "D"
        return answer_circle
    def get_answers(self,list_answers,model):
        results = defaultdict(list)
        list_answers = np.array(list_answers)
        scores = model.predict_on_batch(list_answers / 255.0)
        for idx, score in enumerate(scores):
            question = idx // 4
            if score[1] > 0.9:
                chosed_answer = self.map_answer(idx)
                results[question + 1].append(chosed_answer)

        return results

class crop_image:
    def get_x_ver1(self,s):
        s = cv2.boundingRect(s)
        return s[0] * s[1]
    def pre_processing_input(self,img):
        img = cv2.resize(img,(1056,1500))
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)
        img_canny = cv2.Canny(blurred, 100, 200)
        cnts = cv2.findContours(img_canny.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        mask = np.zeros(img.shape[:2], dtype="uint8")
        return cnts,img 
    def crop_image_sbd(self,img):
        cnts,gray_img = self.pre_processing_input(img)
        info_blocks = []
        x_old, y_old, w_old, h_old = 0, 0, 0, 0
        if len(cnts) > 0:
          cnts = sorted(cnts, key=self.get_x_ver1)
          for i, c in enumerate(cnts):
            x, y, w, h = cv2.boundingRect(c)
            if w * h > 2000 and h < w and h == 34:
              check_xy_min = x * y - x_old * y_old
              check_xy_max = (x + w) * (y + h) - (x_old + w_old) * (y_old + h_old)
              if check_xy_min > 70000 and check_xy_max > 110000:
                print(check_xy_min,check_xy_max)
                info_blocks.append((gray_img[y:y + h, x:x + w],[x,y,w,h]))
                x_old,y_old,w_old,h_old= x,y,w,h
          
        return info_blocks
    def crop_image_md(self,img):
        cnts,gray_img = self.pre_processing_input(img)
        info_blocks = []
        x_old, y_old, w_old, h_old = 0, 0, 0, 0
        if len(cnts) > 0:
          cnts = sorted(cnts, key=self.get_x_ver1)
          for i, c in enumerate(cnts):
            x, y, w, h = cv2.boundingRect(c)
            if w * h > 2000 and h < w and h == 34:
              check_xy_min = x * y - x_old * y_old
              check_xy_max = (x + w) * (y + h) - (x_old + w_old) * (y_old + h_old)
              if check_xy_min > 90000 and check_xy_max > 131000:
                print(check_xy_min,check_xy_max)
                info_blocks.append((gray_img[y:y + h, x:x + w],[x,y,w,h]))
                x_old,y_old,w_old,h_old= x,y,w,h

        return info_blocks
    def split_blocks_sbd(self,a):
        list_answers = []
        for ans_block in a:
          ans_block_img = np.array(ans_block[0])
          offset1 = ceil(ans_block_img.shape[1] / 6)
          h = ans_block_img.shape[0]
          for i in range(6):
            box_img = np.array(ans_block_img[4:h-4,i * offset1+2:(i + 1) * offset1-2])
            list_answers.append(box_img)
        return list_answers
    def split_blocks_md(self,a):
        list_answers = []
        for ans_block in a:
            ans_block_img = np.array(ans_block[0])
            offset1 = ceil(ans_block_img.shape[1] / 3)
            h = ans_block_img.shape[0]
            for i in range(3):
                box_img = np.array(ans_block_img[4:h-4,i * offset1+2:(i + 1) * offset1-2])
                list_answers.append(box_img)
        return list_answers


class predict_sbd_md:
    def get_x_ver1(self, s):
        s = cv2.boundingRect(s)
        return s[0] * s[1]

    def pre_processing_input(self, img):
        img = cv2.resize(img,(1056,1500))
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray_img, (5, 5), 0)
        img_canny = cv2.Canny(blurred, 100, 200)
        cnts = cv2.findContours(img_canny.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        return cnts,img

    def crop_image_sbd(self, img):
        cnts, gray_img = self.pre_processing_input(img)
        info_blocks = []
        x_old, y_old, w_old, h_old = 0, 0, 0, 0
        if len(cnts) > 0:
            cnts = sorted(cnts, key= self.get_x_ver1)
            for i, c in enumerate(cnts):
                x, y, w, h = cv2.boundingRect(c)
                if w * h > 37000 and h > w and w >120 and w<130:
                    check_xy_min = x * y - x_old * y_old
                    check_xy_max = (x + w) * (y + h) - (x_old + w_old) * (y_old + h_old)
                    if check_xy_min > 1000 and check_xy_max > 1000:
                        print(check_xy_min,check_xy_max)
                        info_blocks.append((gray_img[y:y + h, x:x + w],[x,y,w,h]))
                        x_old,y_old,w_old,h_old= x,y,w,h
        return info_blocks

    def crop_image_md(self, img):
        cnts,gray_img = self.pre_processing_input(img)
        info_blocks = []
        x_old, y_old, w_old, h_old = 0, 0, 0, 0
        if len(cnts) > 0:
            cnts = sorted(cnts, key= self.get_x_ver1)
            for i, c in enumerate(cnts):
                x, y, w, h = cv2.boundingRect(c)
                if w * h > 19000 and h > w and w == 65:
                    check_xy_min = x * y - x_old * y_old
                    check_xy_max = (x + w) * (y + h) - (x_old + w_old) * (y_old + h_old)
                    if check_xy_min > 1000 and check_xy_max > 1000:
                        print(check_xy_min,check_xy_max)
                        info_blocks.append((gray_img[y:y + h, x:x + w],[x,y,w,h]))
                        x_old,y_old,w_old,h_old= x,y,w,h         
        return info_blocks

    def split_blocks_sbd(self, a):
        list_answers = []
        for ans_block in a:
            ans_block_img = np.array(ans_block[0])
            h = ans_block_img.shape[0]
            offset1 = ceil(ans_block_img.shape[1] / 6)
            for i in range(6):
                box_img = np.array(ans_block_img[:,i * offset1:(i + 1) * offset1])
                list_answers.append(box_img)
        return list_answers

    def split_blocks_md(self, a):
        list_answers = []
        for ans_block in a:
            ans_block_img = np.array(ans_block[0])
            h = ans_block_img.shape[0]
            offset1 = ceil(ans_block_img.shape[1] / 3)  
            for i in range(3):
                box_img = np.array(ans_block_img[:,i * offset1:(i + 1) * offset1])
                list_answers.append(box_img)
        return list_answers

    def list_ans(self, list_answers):
        list_choices = []
        for answer_img in list_answers:
            start=0
            offset=30
            for i in range(10):
                bubble_choice = answer_img[start + i * offset:start + (i + 1) * offset,:] 
                bubble_choice = cv2.resize(bubble_choice,(28,28),interpolation = cv2.INTER_AREA)
                bubble_choice = cv2.cvtColor(bubble_choice,cv2.COLOR_BGR2GRAY)    
                bubble_choice = cv2.threshold(bubble_choice, 120, 255, cv2.THRESH_BINARY_INV )[1]
                list_choices.append(bubble_choice)
        return list_choices

    def get_answers(self, list_answers):
        results = ""
        model  = tf.keras.models.load_model('weight11.h5')
        list_answers = np.array(list_answers)
        scores = model.predict_on_batch(list_answers/255.0)
        for idx,score in enumerate(scores):
            if score[1] > 0.9:
                chosed_answer = idx%10
                results+= str(chosed_answer)
        return results

        