import cv2
import time
import datetime
'''
1.install firestore package in raspberry Pi
2.Save autoattendance-91502...-.json file in RPi
'''
from google.cloud import firestore
import google.cloud.exceptions

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
    # Section written by jay for save image to database
    db = firestore.Client.from_service_account_json('autoattendance-91502-firebase-adminsdk-f7igv-441ea74b8f.json')
    # create img variable here which contains our captured image
    data = {
        "Image": img
    }
    doc_ref = db.collection('test_images').document(img_name)
    doc_ref.set(data)
    # section end
    print(file_name)
    cv2.imwrite(file_name + ".jpg", frame)
    cap.release()


if __name__ == "__main__":
    photo_click()
    time.sleep(3)
    photo_click()
 # jay k