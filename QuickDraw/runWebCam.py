import cv2
from keras.models import load_model
import numpy as np
from collections import deque
import os

model = load_model('QuickDraw.h5')


def main():
    emojis = get_QD_emojis()
    cap = cv2.VideoCapture(0)
    
    #HSV에서 BGR로 가정할 범위를 정의함
    Lower_blue = np.array([110, 50, 50])
    Upper_blue = np.array([130, 255, 255])
    pts = deque(maxlen=512)
    blackboard = np.zeros((480, 640, 3), dtype=np.uint8)
    digit = np.zeros((200, 200, 3), dtype=np.uint8)
    
    #pred_class 는 이미지의 번호를 나타낸다.
    pred_class = 0

    while (cap.isOpened()):
        ret, img = cap.read()
        img = cv2.flip(img, 1)
        ##cv2.imshow('img',img)
        
        #BGR을 HSV 모드로 전환
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        #픽셀 이미지는 주변 픽셀의 영향을 받게 되므로 가중치를 가진 행렬을 이용해서 이미지에 여러가지 효과를 줄 수 있는데 
        #이 행렬을 커널이라고 한다
        #3 *3 커널이라 함은 이미지를 변환하기 위한 9개의 행렬을 의미하게 된다
        kernel = np.ones((5, 5), np.uint8)
        
        #cv2.inRange(hsv, Lower_blue, Upper_blue) -> 색 추적
        #HSV 이미지에서 청색만 추출하기 위한 임계값
        #범위에 해당하는 부분만 오리지널 값으로 남기고, 이외는 0으로 채워서 반환
        #참고 : http://m.blog.naver.com/samsjang/220504633218
        mask = cv2.inRange(hsv, Lower_blue, Upper_blue)
        
        #cv2.erode(mask, kernel, iterations=2) -> 침식 연산
        #원래 있던 객체의 영역을 깍아 내는 연산
        #아주 작은 노이즈들을 제거할 때 사용
        #참고 : https://webnautes.tistory.com/1257
        mask = cv2.erode(mask, kernel, iterations=2)
        
        #cv2.dilate(mask, kernel, iterations=1) -> 팽창 연산
        #노이즈(작은 흰색 오브젝트)를 없애기 위해 사용한 Erosion에 의해서 작아졌던 오브젝트를 원래대로 돌림
        mask = cv2.dilate(mask, kernel, iterations=1)
        
        #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        #Erosion 연산 다음에 Dilation 연산을 적용
        #이미지 상의 노이즈(작은 흰색 물체)를 제거하는데 사용
        #cv2.MORPH_OPEN -> 열림 연산
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        #cv2.MORPH_CLOSE -> 닫힘 연산
        #오브젝트 안의 노이즈들(검은색) 제거하는데 사용
        mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
        
        #mask = cv2.dilate(mask, kernel, iterations=1)
        ##cv2.imshow("mask", mask)
        
        res = cv2.bitwise_and(img, img, mask=mask)
        cnts, heir = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        center = None

        if len(cnts) >= 1:
            cnt = max(cnts, key=cv2.contourArea)
            if cv2.contourArea(cnt) > 200:
                ((x, y), radius) = cv2.minEnclosingCircle(cnt)
                cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(img, center, 5, (0, 0, 255), -1)
                M = cv2.moments(cnt)
                center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                pts.appendleft(center)
                for i in range(1, len(pts)):
                    if pts[i - 1] is None or pts[i] is None:
                        continue
                    cv2.line(blackboard, pts[i - 1], pts[i], (255, 255, 255), 7)
                    cv2.line(img, pts[i - 1], pts[i], (0, 0, 255), 2)
        elif len(cnts) == 0:
            if len(pts) != []:
                #cv2.cvtColor(blackboard, cv2.COLOR_BGR2GRAY)
                #흑백 색상으로 바꿈
                blackboard_gray = cv2.cvtColor(blackboard, cv2.COLOR_BGR2GRAY)
                blur1 = cv2.medianBlur(blackboard_gray, 15)
                blur1 = cv2.GaussianBlur(blur1, (5, 5), 0)
                
                #https://hoony-gunputer.tistory.com/entry/opencv-python-%EC%9D%B4%EB%AF%B8%EC%A7%80-Thresholding
                #검은 화면에 사용자가 그린 흰색선이 존재하는 이미지가 뜰 것
                thresh1 = cv2.threshold(blur1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                
                ##cv2.imshow("thresh",thresh1)
                
                blackboard_cnts= cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]
                if len(blackboard_cnts) >= 1:
                    cnt = sorted(blackboard_cnts, key=cv2.contourArea, reverse=True)[0]
                    #cnt = max(blackboard_cnts, key=cv2.contourArea)
                    print(cv2.contourArea(cnt))
                    if cv2.contourArea(cnt) > 2000:
                        x, y, w, h = cv2.boundingRect(cnt)
                        digit = blackboard_gray[y:y + h, x:x + w]
                        pred_probab, pred_class = keras_predict(model, digit)
                        #pred_probab 는 1.0 만 나온다. 대체 뭐지?
                        #여기서 pred_class 는 각이미지의 번호를 나타내는듯
                        print("hey!",pred_probab," and ", pred_class)

            pts = deque(maxlen=512)
            blackboard = np.zeros((480, 640, 3), dtype=np.uint8)
            img = overlay(img, emojis[pred_class], 400, 250, 100, 100)
        cv2.imshow("Frame", img)
        
        k = cv2.waitKey(10)
        if k == 27:
            cv2.destroyAllWindows()
            break


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


def overlay(image, emoji, x, y, w, h):
    print("function overlay start")
    try:
        emoji = cv2.resize(emoji, (w, h))
        image[y:y + h, x:x + w] = blend_transparent(image[y:y + h, x:x + w], emoji)
    except :
        pass
    return image

def blend_transparent(face_img, overlay_t_img):
    print("function blend_transparent start")
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:, :, :3]  # Grab the BRG planes
    overlay_mask = overlay_t_img[:, :, 3:]  # And the alpha plane

    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))


keras_predict(model, np.zeros((50, 50, 1), dtype=np.uint8))

if __name__ == '__main__':
    main()