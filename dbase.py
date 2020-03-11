import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from google.cloud import firestore
from google.cloud import exceptions

import datetime
from google.cloud.firestore_v1 import DocumentSnapshot
import os

if (not len(firebase_admin._apps)):
    cred = credentials.Certificate('autoattendance-91502-firebase-adminsdk-f7igv-441ea74b8f.json')
    firebase_admin.initialize_app(cred, {'databaseURL': "https://autoattendance-91502.firebaseio.com"})

        # 'apiKey': "AIzaSyCTBN5WXkpfmIp0uDqHhVgyHXzZ5tcDglM",
        # 'authDomain': "autoattendance-91502.firebaseapp.com",
        # 'databaseURL': "autoattendance-91502",
        # 'projectId': "autoattendance-91502",
        # 'storageBucket': "autoattendance-91502.appspot.com",
        # 'messagingSenderId': "421526185934",
        # 'appId': "1:421526185934:web:97b3b65cbb88a3e5efed9f",
        # 'measurementId': "G-SNJVZR5PXN"



os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:/programmes/Python/mtcnn/Facenet-Real-time-face-recognition-using-deep-learning-Tensorflow-master/autoattendance-91502-firebase-adminsdk-f7igv-441ea74b8f.json"

def get_department_list():
    # function to get list of department
    db = firestore.Client()
    docs = db.collection('Students').stream()
    doc_arr = []
    for doc in docs:
        doc_arr.append(doc.id)
    return doc_arr

def get_subject_list(dept):
    # function to get list of subjects according to department

 def add_student_byid(dept, stud_id, data):

    # [To add students details by ID no.]
    # [Data is a dictionary containing student's name passed by user]
    db = firestore.Client()
    db.collection('Students').document(dept+'/ListOfStudents/'+stud_id).set(data)

def get_student_byId(dept, stud_id):
    # [To get students details in dictionary form]
    db = firestore.Client()
    stud_ref = db.collection('Students').document(dept+'/ListOfStudents/'+stud_id)

    try:
        doc = stud_ref.get()
        print('Document found')
        return doc.to_dict()
    except exceptions.NotFound:
        print('No data found')

def getall_students(dept):
    # [To get data of all students in array of dictionaries]
    db = firestore.Client()
    stud_ref = db.collection('Students').document(dept).collection('ListOfStudents')
    # att_ref = db.collection('Students').document(dept+'/ListOfStudents')
    students = stud_ref.stream()
    stud_array = []
    for stud in students:
        data = stud.to_dict()
        data["stud_id"] = stud.id
        stud_array.append(data)
    return stud_array
'''
    Below written function i.e update_attendance is a very important function so please don't modify it.
'''

def update_attendance(data):
    # [This function is to update attendance every time when the model is run]
    dept = 'DCE'
    date = str(datetime.date.today().strftime('%d-%m-%Y'))
    sub_id = data['sub_id']
    sub_string = data['sub_arr']
    # To update overall total lectures
    db = firestore.Client()
    dept_ref = db.collection('Students').document(dept)
    dept_doc = dept_ref.get()
    dept_doc = dept_doc.to_dict()
    tl = dept_doc['TotalLectures']
    tl = tl+1
    dept_ref.update({
        'TotalLectures':tl
    })
    print("overall lectures updated")
    # overall lectures updated

    # update totalLectures of particular subject
    sub_ref = db.collection('Students').document(dept+'/ListOfSubjects/'+sub_id)
    sub_doc = sub_ref.get()
    if(sub_doc.exists):
        sub_doc = sub_doc.to_dict()
        ta = sub_doc['TotalLectures']
        ta = ta+1
        dataa = {
            'TotalLectures': ta
        }
        sub_ref.update(dataa)
        print("TotalLectures subjectwise updated")
    # TotalLectures updated
    else:
        print("{} subject not exist".format(sub_id))

    # update Attendance collection datewise
    dataa = {
        sub_id: sub_string
    }
    att_ref = db.collection('Students').document(dept + '/Attendance/' + date)
    doc = att_ref.get()
    if(doc.exists):
        att_ref.update(dataa)
    else:
        att_ref.set(dataa)
    print('Datewise attendance updated')
    # Attendance collection updated

    # update student's subjectwise attendance
    sub_total = sub_ref.get().to_dict()['TotalLectures']
    lec_total = db.collection('Students').document(dept).get().to_dict()['TotalLectures']
    students = db.collection('Students').document(dept).get().to_dict()['TotalStudents']+ 1
    for i in range(1,students):
        stud_id = '18dce00'+str(i)
        if(stud_id in sub_string):
            stud_ref = db.collection('Students').document(dept+'/ListOfStudents/'+stud_id+'/attedent/subwise')
            stud_doc = stud_ref.get()
            stud_doc = stud_doc.to_dict()
            subper = stud_doc[sub_id]
            total = stud_doc['total']
            total = total + 1
            subper = subper + 1
            stud_ref.update({
                    sub_id:subper,
                    'total':total
            })
            subpercentage = subper/sub_total*100
            overallper = total/lec_total*100
            stud_ref = db.collection('Students').document(dept + '/ListOfStudents/' + stud_id + '/attedent/subwise_percentage').update({
                sub_id:subpercentage,
                'total':overallper
            })
        else:
            stud_ref = db.collection('Students').document(dept + '/ListOfStudents/' + stud_id + '/attedent/subwise')
            stud_doc = stud_ref.get()
            stud_doc = stud_doc.to_dict()
            subper = stud_doc[sub_id]
            total = stud_doc['total']
            subpercentage = subper / sub_total * 100
            overallper = total/lec_total * 100
            stud_ref = db.collection('Students').document(
                dept + '/ListOfStudents/' + stud_id + '/attedent/subwise_percentage').update({
                sub_id: subpercentage,
                'total':overallper
            })

    print("Student wise attendance updated")
    # [Update attendance completed]

def get_stud_subwise(dept,stud_id):
    # [Function to get student's subjectwise percentage attendance]
    # for pie graph
    db = firestore.Client()
    stud_ref = db.collection('Students').document(dept+'/ListOfStudents/'+stud_id).collection('attedent').document('subwise_percentage')
    stud_doc = stud_ref.get()
    doc = stud_doc.to_dict()
    subwise = [v for v in doc.values()]
    # total = subwise[-1]
    subwise.pop(-1)
    data = {
        'stud_id':stud_id,
        'subwise':subwise,
        # 'total':total
    }
    return data
    # function ended

def get_sub_studwise_datewise(dept,date,sub_id):
    # [Function to get subject's studentwise attendance on particular date]
    db = firestore.Client()
    try:
        sub_ref = db.collection('Students').document(dept+'/Attendance/'+date).get().to_dict()
        return sub_ref[sub_id]
    except exceptions.NotFound:
        return ("Data not found")
    # function ended

def get_sub_studwise(dept,sub_id):
    # [Function to get studentwise overall attendance of particular subject]
    db = firestore.Client()
    tot_stud = db.collection('Students').document(dept).get().to_dict()['TotalStudents']+1
    sub_total = []
    for i in range(1,tot_stud):
        stud_id = '18dce00'+str(i)
        subt = db.collection('Students').document(dept+'/ListOfStudents/'+stud_id+'/attedent/subwise_percentage').get().to_dict()
        data = {
            'stud_id':stud_id,
            'total_subwise':subt[sub_id]
        }
        sub_total.append(data)
    return sub_total
    # function ended


'''
Below function is incomplete
'''

def update_by_teacher(dept,date,email,operation,stud_id):

    db = firestore.Client()
    teach_ref = db.collection('Students').document(dept).collection('ListOfSubjects')
    teachers = teach_ref.stream()
    att_ref = db.collection('Students').document(dept+'/Attendance/'+date).get()
    for teach in teachers:
        teach_doc = teach.to_dict()
        em = teach_doc['teach_email']
        # print(em)
        if(em==email):
            sub_id = teach_doc['sub_id']
            att_doc = att_ref.to_dict()
            print(att_doc)
            sub_arr = att_doc[sub_id]
            if(operation=='delete'):
                var = sub_arr.index(stud_id)
                sub_arr.pop(var)
                # print(sub_arr)
                data = {
                    sub_id: sub_arr
                }
                att_ref = db.collection('Students').document(dept + '/Attendance/' + date)
                doc = att_ref.get()
                if (doc.exists):
                    att_ref.update(data)
                else:
                    att_ref.set(data)

            elif(operation=='add'):
                sub_arr.append(stud_id)
                data = {
                    sub_id: sub_arr
                }
                att_ref = db.collection('Students').document(dept + '/Attendance/' + date)
                doc = att_ref.get()
                if (doc.exists):
                    att_ref.update(data)
                else:
                    att_ref.set(data)
















# if __name__ == "__main__":
#     db = firestore.Client()
#
#     for i in range(1,8):
#         stud_id = '18dce00' + str(i)
#         stud_ref = db.collection('Students').document('DCE/ListOfStudents/'+stud_id).collection('attedent').document('subwise_percentage').update({
#             'total':0
#         }
#         )
#
#







