import os
import time
from sys import exit
from cv2 import cv2
import platform
from libSQL import libSQL
from libFace import libFace
from mlx import MLX90614

# 在视频窗口左上方上打印文字
def putTextLog(text):
    global title
    global img
    global logTop
    logTop += 30
    cv2.putText(img, text, (0, logTop),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
    cv2.imshow(title, img)
    cv2.waitKey(1)


# 设定参数
title = 'system'

os.chdir(os.path.split(os.path.realpath(__file__))[0])

print('初始化...')
db = libSQL()
face = libFace()
mlx = MLX90614()

print('获取用户信息...')
users, successList = db.getUsers()

print('初始化人脸库...')
face.load()
face.need(users)
face.removeOld()
face.download(users)
face.gen(users)
face.save()

print('进入打卡系统')
vc = cv2.VideoCapture(0)

count = 0

while True:
    ret, img = vc.read()
    if not ret:
        print('No Capture.')
        break

    face_locations, _ = face.detect(img)

    if len(face_locations) > 0:
        count += 1
    else:
        count = 0

    for (top, right, buttom, left) in face_locations:
        cv2.rectangle(img, (left, top), (right, buttom), (0, 255, 0), 2)
        cv2.imshow(title, img)
        cv2.waitKey(1)

    if count < 3:
        cv2.imshow(title, img)
        cv2.waitKey(1)
        continue

    face_encodings = face.encode(img, face_locations)

    for face_encodeing in face_encodings:

        count = 0
        logTop = 0

        uid = face.match(face_encodeing)
        
        if uid == 'unknown' or uid not in users:
            putTextLog('Find unknown user')
            break
        elif uid in successList:
            putTextLog('Find %s' % users[uid]['name'])
            putTextLog('You have checked')
            time.sleep(1)
            break

        putTextLog('Find %s' % users[uid]['name'])

        putTextLog('Keep your hand on sensor')
        cv2.waitKey(1000)

        temp = mlx.get_human_temp()

        if temp == -1:
            putTextLog('Timeout')
            cv2.waitKey(1000)
            break

        status = 'safety' if (temp < 37.3) else 'warning'

        putTextLog('Temp: %s, Status: %s' % (str(temp), status))
        putTextLog('Success')

        print('Uid: %s, 打卡成功' % uid)
        successList.append(uid)
        db.setUser(uid, temp, status)
        cv2.waitKey(3000)

    cv2.imshow(title, img)
    if cv2.waitKey(1) != -1:
        vc.release()
        cv2.destroyAllWindows()
        exit()

