import cv2
import os
from tkinter import *
import train_main

img = cv2.VideoCapture(0)
case = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


def exit_code():
    exit()

def face_recognizer(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = case.detectMultiScale(gray, 1.32, 5)
    if faces is():
        return None
    for (x, y, w, h) in faces:
        croaped_faces = img[y:y+h, x:x+w]

    return croaped_faces

def photo_taker():
    a = folder_name.get()
    print(a)
    path = "faces/" + a + "/"
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)

    cap = cv2.VideoCapture(0)
    count = 0
    while True:

        ret, frame = cap.read()
        if face_recognizer(frame) is not None:
            count += 1
            face = cv2.resize(face_recognizer(frame), (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            File_path = path + "/" + str(count) + ".jpg"
            cv2.imwrite(File_path, face)
            cv2.putText(frame, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow("face", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            if count == 120:
                break
        else:
            print("face not found")
    cv2.destroyAllWindows()
    cap.release()
    train_main.train()


windows = Tk()
windows.geometry("640x640")
windows.title("Face Data Maker")

# title
label1 = Label(windows, text="WELCOME TO FACE DATA MAKER", fg="blue", bg="yellow",
               relief="solid", width=30, font=('arial', 20, 'bold'))
label1.place(x=55, y=53)

# Name box
folder_name = StringVar()
label2 = Label(windows, text="Enter Your Full Name : ", font=('arial', 12, 'bold'))
label2.place(x=75, y=150)

# Name box input
value = Entry(windows, textvar=folder_name)
value.place(x=275, y=150)
value.config(width=50)

# Branch drop down menu
label3 = Label(windows, text="Branch :", width=10, font=('arial', 12, 'bold'))
label3.place(x=75, y=200)
list1 = ['Computer', 'IT', "civil", "Mechanical", "Chemical", "EC"]
var = StringVar()
droplist = OptionMenu(windows, var, *list1)
var.set("Select Branch")
droplist.place(x=155, y=200)

# Year drop down menu
list2 = [1, 2, 3]
label4 = Label(windows, text="Year :", width=10, font=('arial', 12, 'bold'))
label4.place(x=255, y=200)
var1 = StringVar()
var1.set("Select Year")
droplist1 = OptionMenu(windows, var1, *list2)
droplist1.place(x=355, y=200)

# exit button
b1 = Button(windows, text="Exit", width=10, bg="black", fg="white", command=exit_code)
b1.place(x=180, y=320)

# image taker button
b2 = Button(windows, text="Click Images", width=15, bg="black", fg="white", command=photo_taker)
b2.place(x=280, y=320)
windows.mainloop()





