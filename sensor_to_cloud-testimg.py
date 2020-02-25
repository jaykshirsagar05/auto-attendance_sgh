import cv2
import time
import datetime
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('autoattendance-91502-firebase-adminsdk-f7igv-441ea74b8f.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'autoattendance-91502.appspot.com'
})

def photo_click():
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    file = str(datetime.date.today()).split("-")
    file_name = ""
    file_name = file_name.join(file)
    t = time.localtime()
    file = time.strftime("%H:%M:%S", t).split(":")
    a = ''
    file_name = file_name + a.join(file)
    # store in PI
    cv2.imwrite(file_name + ".jpg", frame)
    cap.release()
    bucket = storage.bucket()
    imageBlob = bucket.blob(file_name)
    # upload to cloud
    imageBlob.upload_from_filename(filename=os.getcwd() + '\\' + file_name + '.jpg')
    print(file_name)
    # delete file from PI
    try:
        os.remove(os.getcwd() + '\\' + file_name + '.jpg')
    except: pass

if __name__ == "__main__":
    photo_click()
    time.sleep(3)
    photo_click()
