from functools import partial
from tkinter import *
import boto3
import mutagen
from pygame import *
import pygame,sys

s3=boto3.client('s3',
   aws_access_key_id='',
   aws_secret_access_key='')

arr1=[]
arr2=[]
arr3=[]
arr4=[]
arr5=[]
arr6=[]

count=0
for object in s3.list_objects(Bucket='')['Contents']:
    s3.download_file('', object['Key'], object['Key'])
    arr1.append(object['Key'])

for object in s3.list_objects(Bucket='')['Contents']:
    s3.download_file('', object['Key'], object['Key'])
    arr2.append(object['Key'])

for object in s3.list_objects(Bucket='')['Contents']:
    s3.download_file('', object['Key'], object['Key'])
    arr3.append(object['Key'])

for object in s3.list_objects(Bucket='')['Contents']:
    s3.download_file('', object['Key'], object['Key'])
    arr4.append(object['Key'])

for object in s3.list_objects(Bucket='')['Contents']:
    s3.download_file('', object['Key'], object['Key'])
    arr5.append(object['Key'])

for object in s3.list_objects(Bucket='')['Contents']:
    s3.download_file('', object['Key'], object['Key'])
    arr6.append(object['Key'])

#until this line is upload text and mp3 file.

#일단 스파게티로 가자...! 코드는 나중에 수정하고 돌아가기만 하면 돼!

def raise_frame_first(frame):#f1
    frame.tkraise()
    frame.configure(background='MistyRose')

    Label(frame, width=16, background='MistyRose', font=('Helvetica', 18, "bold")).pack(side='left')
    Label(frame, width=13, background='MistyRose', font=('Helvetica', 18, "bold")).pack(side='right')
    Label(frame, text="  ", background='MistyRose', font=('Helvetica', 4, "bold")).pack()
    Label(frame, text="Are you want to listen?",background='MistyRose',relief="solid", font=('Helvetica', 18, "bold")).pack(side='top', ipadx=50 ,ipady=10)
    Label(frame, text="  ", background='MistyRose', font=('Helvetica', 4, "bold")).pack()

    Button(frame, width=10, text='News\u2710', background='white', font=('Helvetica', 18), command=lambda: raise_frame_sex(f3,arr1,arr2)).pack(ipadx=10)
    Label(frame, text="  ", background='MistyRose', font=('Helvetica', 4, "bold")).pack()
    Button(frame, width=10, text='Fairy\u2728‍', background='white', font=('Helvetica', 18),command=lambda: raise_frame_sex(f3,arr3,arr4)).pack(ipadx=10)
    Label(frame, text="  ", background='MistyRose', font=('Helvetica', 4, "bold")).pack()
    Button(frame, width=10, text='Android\u2709', background='white', font=('Helvetica', 18),command=lambda: raise_frame_cate(f4,arr5,arr6,"none")).pack(ipadx=10)

    for widget in f2.winfo_children():#f2 frame clear
        widget.destroy()
    f2.pack_forget

    for widget in f3.winfo_children():#f2 frame clear
        widget.destroy()
    f3.pack_forget

    for widget in f4.winfo_children():#f2 frame clear
        widget.destroy()
    f4.pack_forget




def raise_frame_sex(frame,arrA,arrB):#f3
    frame.tkraise()
    frame.configure(background='MistyRose')


    Label(frame, height=4, text='',background='MistyRose', font=('Helvetica', 18, "bold")).pack(side='top')
    Button(frame, width=15,  text='Man',bg='white', font=('Helvetica', 18),command=lambda:raise_frame_cate(f4,arrA,arrB,"man")).pack()
    Button(frame, width=15, text='Woman',bg='white', font=('Helvetica', 18),command=lambda:raise_frame_cate(f4,arrA,arrB,"woman")).pack()

    for widget in f1.winfo_children():#f2 frame clear
        widget.destroy()
    f1.pack_forget

    for widget in f2.winfo_children():#f2 frame clear
        widget.destroy()
    f2.pack_forget

    for widget in f4.winfo_children():
        widget.destroy()
    f4.pack_forget



def raise_frame_cate(frame,arrA,arrB,sex):#f4
    frame.tkraise()
    frame.configure(background='MistyRose')
    pygame.mixer.music.stop()

    if arrA==arr1 or arrA==arr2:
        Label(frame, text="\u2710", background='MistyRose', font=('Helvetica', 40)).pack(side="top", fill="x", pady=5)
    elif arrA==arr3 or arrA==arr4:
        Label(frame, text="\u2728", background='MistyRose', font=('Helvetica', 40)).pack(side="top", fill="x", pady=5)
    elif arrA==arr5 or arrA==arr6:
        Label(frame, text="\u2709", background='MistyRose', font=('Helvetica', 40)).pack(side="top", fill="x", pady=5)
    for i in range(len(arrB)):
        Button(frame, width=25, text=arrB[i][:len(arrB[i])-4],bg='white',font=('Helvetica', 10), command=lambda x=i:raise_frame(f2,x,arrB,arrA,sex)).pack()
        Label(frame, text="  ", background='MistyRose', font=('Helvetica', 4, "bold")).pack()
    Button(frame, width=25, text='Back',bg='white', font=('Helvetica', 10),command=lambda:raise_frame_first(f1)).pack()

    for widget in f1.winfo_children():
        widget.destroy()
    f1.pack_forget

    for widget in f2.winfo_children():
        widget.destroy()
    f2.pack_forget

    for widget in f3.winfo_children():
        widget.destroy()
    f3.pack_forget

def raise_frame(frame,i,arrA,arrB,sex):#f2
    frame.tkraise()
    frame.configure(background='MistyRose')
    pygame.init()
    pygame.mixer.init()
    print (arrB)
    print (arrA)
    print (i)
    if arrA==arr6:
        myfile = open(arrA[i], 'r',encoding='utf-8')
    else:
        myfile = open(arrA[i], 'r', encoding=None)
    mystring = myfile.read()
    #잠만 이게 지금 B에 다 돌면서
    play=''
    if sex=='woman':
        for j in range(len(arrB)):
            if arrB[j][0:len(arrB[j])-10]==arrA[i][0:len(arrA[i])-4]:
                play=arrB[j][0:len(arrB[j])-10]+"_woman.mp3"
                break

    elif sex=='man':
        for j in range(len(arrB)):
            if arrB[j][0:len(arrB[j])-8]==arrA[i][0:len(arrA[i])-4]:
                play=arrB[j][0:len(arrB[j])-8]+"_man.mp3"
                break
    else:
        play=arrB[i]

    print(play)



    pygame.mixer.music.load(play)
    pygame.mixer.music.play()
    if arrB==arr5:
        Label(frame, text=arrB[i][0:len(arrB[i]) - 4], background='MistyRose', font=('Helvetica', 23,)).pack(ipadx=10,ipady=10)
    else:
        Label(frame, text=arrB[i][0:len(arrB[i]) - 8],background='MistyRose',font=('Helvetica', 23,)).pack(ipadx=10,ipady=10)

    Label(frame, text="  ", background='MistyRose', font=('Helvetica', 4, "bold")).pack()
    Label(frame, text=mystring ,background='white', relief="solid", font=('Helvetica', 12 )).pack(ipadx=30,ipady=30)
    print(arrB[i]+"aa")

    Label(frame, text="  ", background='MistyRose', font=('Helvetica', 4, "bold")).pack()
    Button(frame, width=25,text='Back',bg='white', font=('Helvetica', 18),command=lambda: raise_frame_cate(f4,arrB,arrA,sex)).pack()

    myfile.close()


    for widget in f1.winfo_children():#f1 frame clear
        widget.destroy()
    f1.pack_forget

    for widget in f3.winfo_children():#f1 frame clear
        widget.destroy()
    f3.pack_forget

    for widget in f4.winfo_children():#f1 frame clear
        widget.destroy()
    f4.pack_forget


root = Tk()
root.geometry("800x450")
root.title("Turingbot")
root.configure(background='MistyRose')
pygame.init()
pygame.mixer.init()
f1 = Frame(root)
f2 = Frame(root)
f3 = Frame(root)
f4 = Frame(root)

for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')


#Label(f4, text='FRAME 4').pack()
Button(f4, text='Goto to frame 1', command=lambda:raise_frame_first(f1)).pack()

raise_frame_first(f1)
root.mainloop()

