import cv2
import time
import datetime


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
    print(file_name)
    cv2.imwrite(file_name + ".jpg", frame)
    cap.release()


if __name__ == "__main__":
    photo_click()
    time.sleep(3)
    photo_click()
