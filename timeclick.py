import cv2
import time
import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': autoattendance-91502,
})

db = firestore.client()


def photo_click():
    count = 0
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    file = str(datetime.date.today()).split("-")
    file_name = ""
    file_name = file_name.join(file)
    t = time.localtime()
    file = time.strftime("%H:%M:%S", t).split(":")
    a = ''
    file_name = file_name + a.join(file)
    img_name = file_name
    img = cap.read()
    #Section written by jay for save image to database
    data = {
        "Image": img
    }
    doc_ref = db.collection('test_images').document(img_name)
    doc_ref.set(data)
    #section end
    print(file_name)
    cv2.imwrite(file_name + ".jpg", frame)
    cap.release()


if __name__ == "__main__":
    photo_click()
    time.sleep(3)
    photo_click()
