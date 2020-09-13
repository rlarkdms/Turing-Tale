## 목표 clear 기능 돌아가게 만들기

import cv2
from PIL import ImageTk, Image, ImageDraw
import PIL
from tkinter import *

import os.path
from keras.models import load_model
import numpy as np
from collections import deque
import os
from playsound import playsound

from PIL import ImageTk,ImageGrab,Image

width = 400
height = 400
center = height//2
white = (255, 255, 255)
green = (0,128,0)

def clear():
    ##Clear 에 대한 생각을 변경
    ## 현재 내가 사용하는 코드에선 사용자에게 보이는 line 과 컴퓨터가 인식하는 line 두가지가 존재
    ## 컴퓨터가 인식하는 line 을 지우는 것이 아닌 엄청 두꺼운 흰색 선을 다시 그리게 함으로써 캔버스를 깨끗이 한 것 같은 효과 줌
    cv.delete ("all")
    filename = "saveImage\\image.png"
    draw.line((0, 0, 400, 0),fill="white",width=800)
    image.save(filename)

def predict():
    filename = "saveImage\\image.png"
    image.save(filename)
    
    model = load_model('QuickDraw.h5')
    file = 'saveImage\\image.png'
    emojis = get_QD_emojis()


    if os.path.isfile(file):
        print("Yes. it is a file")
        src = cv2.imread(file, cv2.IMREAD_COLOR)
        dst = cv2.bitwise_not(src)

        blackboard_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        blur1 = cv2.medianBlur(blackboard_gray, 1)
        blur1 = cv2.GaussianBlur(blur1, (5, 5), 0)

        thresh1 = cv2.threshold(blur1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        blackboard_cnts= cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

        if len(blackboard_cnts) >= 1:
            cnt = sorted(blackboard_cnts, key=cv2.contourArea, reverse=True)[0]
            print(cv2.contourArea(cnt))
            if cv2.contourArea(cnt) > 2000:
                x, y, w, h = cv2.boundingRect(cnt)
                digit = blackboard_gray[y:y + h, x:x + w]
                pred_probab, pred_class = keras_predict(model, digit)
                #여기서 pred_class 는 각이미지의 번호를 나타내는듯
                print("hey!",pred_probab," and ", pred_class)
                result_path1 = 'qd_emo\\'
                result_path2 = '.png'
                result = result_path1+str(pred_class)+result_path2
                print(result)
                img = cv2.imread(result, cv2.IMREAD_COLOR)
                resultImage = ImageTk.PhotoImage(file=result)
                label.configure(image=resultImage)
                label.image = resultImage # keep a reference!
#                 print("DONE!")
                #2020-08-18 그림 인식 시 어떤 그림인지 텍스트로 표현
                if pred_class==0:
                    text.set("This is apple!")
                elif pred_class==1:
                    text.set("This is Book!")
                elif pred_class==2:
                    text.set("This is Bowtie!")
                elif pred_class==3:
                    text.set("This is Broom!")
                elif pred_class==4:
                    text.set("This is Candle!")
                elif pred_class==5:
                    text.set("This is Door!")
                elif pred_class==6:
                    text.set("This is Envelope!")
                elif pred_class==7:
                    text.set("This is Fish!")
                elif pred_class==8:
                    text.set("This is Guitar!")
                elif pred_class==9:
                    text.set("This is Ice Cream!")
                elif pred_class==10:
                    text.set("This is Lightning!")
                elif pred_class==11:
                    text.set("This is Moon!")
                elif pred_class==12:
                    text.set("This is Mountain!")
                elif pred_class==13:
                    text.set("This is Star!")
                elif pred_class==14:
                    text.set("This is Tent!")
                elif pred_class==15:
                    text.set("This is Wristwatch!")
                
    elif os.path.isdir(file):
        print("Yes. it is a directory")
    elif os.path.exists(file):
        print("Something exist")
    else :
        print("Nothing")
        
def voice():
    model = load_model('QuickDraw.h5')
    file = 'saveImage\\image.png'
    emojis = get_QD_emojis()


    if os.path.isfile(file):
        print("Yes. it is a file")
        src = cv2.imread(file, cv2.IMREAD_COLOR)
        dst = cv2.bitwise_not(src)

        blackboard_gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        blur1 = cv2.medianBlur(blackboard_gray, 1)
        blur1 = cv2.GaussianBlur(blur1, (5, 5), 0)

        thresh1 = cv2.threshold(blur1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        blackboard_cnts= cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

        if len(blackboard_cnts) >= 1:
            cnt = sorted(blackboard_cnts, key=cv2.contourArea, reverse=True)[0]
            print(cv2.contourArea(cnt))
            if cv2.contourArea(cnt) > 2000:
                x, y, w, h = cv2.boundingRect(cnt)
                digit = blackboard_gray[y:y + h, x:x + w]
                pred_probab, pred_class = keras_predict(model, digit)
                if pred_class==0:
                    playsound('saveAudio\\sampleAudio.mp3')
                
    elif os.path.isdir(file):
        print("Yes. it is a directory")
    elif os.path.exists(file):
        print("Something exist")
    else :
        print("Nothing")

def paint(event):
    # python_green = "#476042"
    x1, y1 = event.x, event.y
    if cv.old_coords:
        x2, y2 = cv.old_coords
        ## 사용자에게 시각적으로 보여주기 위한 line
        cv.create_line(x1, y1, x2, y2, fill="black",width=5)
        ## 실제로 컴퓨터가 인식하는 line
        draw.line([x1, y1, x2, y2],fill="black",width=5)
    cv.old_coords = x1, y1
    
def reset_coords(event):
    cv.old_coords = None
    
###

def keras_predict(model, image):
    print("function keras_predict start")
    processed = keras_process_image(image)
    print("processed: " + str(processed.shape))
    pred_probab = model.predict(processed)[0]
    pred_class = list(pred_probab).index(max(pred_probab))
    return max(pred_probab), pred_class


def keras_process_image(img):
    print("function keras_process_image start")
    image_x = 28
    image_y = 28
    img = cv2.resize(img, (image_x, image_y))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (-1, image_x, image_y, 1))
    return img

def get_QD_emojis():
    print("function get_QD_emojis start")
    emojis_folder = "qd_emo/"
    emojis = []
    for emoji in range(len(os.listdir("qd_emo/"))):
        print(emoji)
        emojis.append(cv2.imread(emojis_folder + str(emoji) + '.png', -1))
    return emojis


root = Tk()
root.geometry("800x420")

# Tkinter create a canvas to draw on
cv = Canvas(root, width=width, height=height, bg='white')
cv.old_coords = None

# PIL create an empty image and draw object to draw on
# memory only, not visible
image = PIL.Image.new("RGB", (width, height), white)
draw = ImageDraw.Draw(image)

#expand=True, fill="both"
cv.place(x=0, y=0, width=400, height=400)
cv.bind("<B1-Motion>", paint)
cv.bind("<ButtonRelease-1>", reset_coords)
root.bind("<Escape>", lambda e: root.destroy())

text= StringVar(root)
text.set("그림을 그리면 알아맞출게요!\n")
# text.configure(state="disabled")
textlabel = Label(root, textvariable=text)
textlabel.place(x=400, y=0, width=400, height=30)

predImage = ImageTk.PhotoImage(file="saveImage\\smile.jpg")
label=Label(root,image=predImage)
label.place(x=400, y=20, width=400, height=360)


button=Button(text="clear",command=clear)
button.place(x=0, y=400, width=100, height=20)

button=Button(text="predict",command=predict)
button.place(x=300, y=400, width=100, height=20)

button=Button(text="voice",command=voice)
button.place(x=550, y=350, width=100, height=20)


root.mainloop()