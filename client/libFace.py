import os
import json
import pickle
import requests
from hashlib import md5
from cv2 import cv2
import face_recognition

def md5_file(filename):
    m = md5()
    with open(filename,'rb') as f:
        for line in f:
            m.update(line)
    md5code = m.hexdigest()
    return md5code

class libFace():

    def __init__(self, dir='faces', saveFilename='save.bin'):
        self.dir = dir
        self.saveFile = dir + '/' + saveFilename
        self.ids = []
        self.encodings = []
        self.classfier = cv2.CascadeClassifier(
            r"D:\opencv\build\etc\haarcascades\haarcascade_frontalface_alt.xml")

    def load(self):
        try:
            with open(self.saveFile, 'rb') as f:
                known_face = pickle.load(f)
            for k, v in known_face.items():
                self.ids.append(k)
                self.encodings.append(v)
            return True
        except Exception:
            return False

    def save(self):
        known_face = {}
        for uid, encoding in zip(self.ids, self.encodings):
            known_face[uid] = encoding
        with open(self.saveFile, 'wb') as f:
            pickle.dump(known_face, f)

    def download(self, users):
        count = 0
        for user in users.values():
            filename = self.dir + '/' + user['id'] + '.jpg'
            if user['id'] not in self.ids or not os.path.exists(filename):
                if user['url'] == '':
                    print("libFace: No url for uid: %s." % user['id'])
                    continue
                response = requests.get(user['url'])
                if response.status_code == 200:
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    count += 1
                else:
                    print("libFace: Download %s.jpg fail." % user['id'])
        return count

    def removeOld(self):
        mlist = requests.get("http://domain.com/daka/api.php?type=md5")
        if mlist.status_code != 200:
            return
        mlist = json.loads(mlist.text)
        filenames = os.listdir(self.dir)
        for filename in filenames:
            uid, ext = os.path.splitext(filename)
            path = self.dir + '/' + filename
            if ext != '.jpg':
                continue
            if filename in mlist and md5_file(path) != mlist[filename]:
                print('libFace: remove %s' % filename)
                os.remove(path)
                index = self.ids.index(uid)
                self.ids.pop(index)
                self.encodings.pop(index)

    def gen(self, users):
        filenames = os.listdir(self.dir)
        for filename in filenames:
            uid, ext = os.path.splitext(filename)
            if ext != '.jpg':
                continue
            if uid not in self.ids and uid in users:
                encoding = face_recognition.face_encodings(
                    cv2.imread(self.dir + '/' + filename))
                if len(encoding) > 0:
                    self.ids.append(uid)
                    self.encodings.append(encoding[0])

    def detect(self, img):
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faceRects = faceRects = self.classfier.detectMultiScale(
            grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        locations = []
        for x, y, w, h in faceRects:
            locations.append((y, x+w, y+h, x))
        return locations, faceRects

    def encode(self, img, locations=None):
        if locations is None:
            return face_recognition.face_encodings(img)
        else:
            return face_recognition.face_encodings(img, locations)

    def match(self, encoding):
        uid = 'unknown'
        matchs = face_recognition.compare_faces(self.encodings, encoding)
        for match, known_id in zip(matchs, self.ids):
            if match:
                uid = known_id
                break
        return uid

    def need(self, users):
        ids = []
        encodings = []
        for uid in self.ids:
            if uid in users:
                index = self.ids.index(uid)
                ids.append(uid)
                encodings.append(self.encodings[index])
        self.ids = ids
        self.encodings = encodings

if __name__ == "__main__":
    face = libFace()
    face.removeOld()
