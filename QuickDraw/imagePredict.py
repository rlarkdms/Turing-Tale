## pygame 으로 실행할 시 mp3 1개 파일에 대한 재생이 무한히 반복되는 문제 발생

import cv2
from PIL import ImageTk, Image, ImageDraw
import PIL
from tkinter import *

import os.path
from keras.models import load_model
import numpy as np
from collections import deque
import os
# from playsound import playsound 교체
import pygame, mutagen.mp3

from PIL import ImageTk,ImageGrab,Image

width = 400
height = 400
center = height//2
white = (255, 255, 255)
green = (0,128,0)

global flag
flag= 0

def clear():
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
                #list 에서 빼옴으로써 if 문 나열을 하지 않게 만들것!
                predict_data = {0:"cloud",1:"lightning",2:"moon",3:"rain",4:"rainbow",5:"snowflake",6:"star",7:"sun",8:"tornado"}
                
                x, y, w, h = cv2.boundingRect(cnt)
                digit = blackboard_gray[y:y + h, x:x + w]
                pred_probab, pred_class = keras_predict(model, digit)

                print("hey!",pred_probab," and ", pred_class)
                result_path1 = 'qd_emo\\'
                result_path2 = '.png'
                result = result_path1+str(pred_class)+result_path2
                print(result)
                img = cv2.imread(result, cv2.IMREAD_COLOR)
                resultImage = ImageTk.PhotoImage(file=result)
                label.configure(image=resultImage)
                label.image = resultImage # keep a reference!
                
                robot_answer = predict_data[pred_class]
                text.set(robot_answer)
                

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
                print("heyhey!",pred_probab," and ", pred_class)
                
                global flag
                print(flag)
                voice_name = pred_class

                if flag ==0:
                    #Female Voice
                    sound_dir = "saveAudio\\female\\"+str(voice_name)+".mp3"
                    print(sound_dir)
                    ## https://kkamikoon.tistory.com/135 참고
                    ## 그는 신이야!
                    playmusic(sound_dir)
                    stopmusic()
                elif flag ==1:
                    #Male Voice
                    sound_dir = "saveAudio\\male\\"+str(voice_name)+".mp3"
                    playmusic(sound_dir)
                    stopmusic()
                
    elif os.path.isdir(file):
        print("Yes. it is a directory")
    elif os.path.exists(file):
        print("Something exist")
    else :
        print("Nothing")
        
def playmusic(soundfile):
    """Stream music with mixer.music module in blocking manner.
       This will stream the sound from disk while playing.
    """
    pygame.init()

    bitsize = -16   # signed 16 bit. support 8,-8,16,-16
    channels = 1    # 1 is mono, 2 is stereo
    buffer = 2048   # number of samples (experiment to get right sound)
    mp3 = mutagen.mp3.MP3(soundfile)
    frequency=mp3.info.sample_rate
    
    pygame.mixer.init()
    clock= pygame.time.Clock()
    pygame.mixer.music.load(soundfile)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
#         print("Playing... - func => playingmusic")
        clock.tick(1000)

def stopmusic():
    """stop currently playing music"""
    pygame.mixer.music.stop()

        
def flag():
    global flag
    
    if flag==0:
        flag=1
    else:
        flag=0

def paint(event):
    # python_green = "#476042"
    x1, y1 = event.x, event.y
    if cv.old_coords:
        x2, y2 = cv.old_coords
        cv.create_line(x1, y1, x2, y2, fill="black",width=5)
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
    print("keras_predict pred_probab = ",pred_probab)
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
text.set("Draw a picture and I'll guess!\n")
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

button=Button(text="Flag",command=flag)
button.place(x=760, y=380, width=40, height=40)
flag = 0


root.mainloop()