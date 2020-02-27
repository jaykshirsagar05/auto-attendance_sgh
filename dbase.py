import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from google.cloud import firestore
from google.cloud import exceptions
from google.cloud.firestore_v1 import DocumentSnapshot

cred = credentials.Certificate('autoattendance-91502-firebase-adminsdk-f7igv-441ea74b8f.json')
firebase_admin.initialize_app(cred, {

    'apiKey': "AIzaSyCTBN5WXkpfmIp0uDqHhVgyHXzZ5tcDglM",
    'authDomain': "autoattendance-91502.firebaseapp.com",
    'databaseURL': "autoattendance-91502",
    'projectId': "autoattendance-91502",
    'storageBucket': "autoattendance-91502.appspot.com",
    'messagingSenderId': "421526185934",
    'appId': "1:421526185934:web:97b3b65cbb88a3e5efed9f",
    'measurementId': "G-SNJVZR5PXN"

})

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

        stud_array.append(stud.to_dict())

    return stud_array
'''
    Below written function i.e update_attendance is a very important function so please don't modify it.
'''

def update_attendance(dept,date,sub_id,sub_string):
    # [This function is to update attendance every time when the model is run]

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
    sub_doc = sub_doc.to_dict()
    ta = sub_doc['TotalLectures']
    ta = ta+1
    data = {
        'TotalLectures': ta
    }
    sub_ref.update(data)
    print("TotalLectures subjectwise updated")
    # TotalLectures updated

    # update Attendance collection datewise
    data = {
        sub_id: sub_string
    }
    att_ref = db.collection('Students').document(dept + '/Attendance/' + date)
    doc = att_ref.get()
    if(doc.exists):
        att_ref.update(data)
    else:
        att_ref.set(data)
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
    db = firestore.Client()
    stud_ref = db.collection('Students').document(dept+'/ListOfStudents/'+stud_id).collection('attedent').document('subwise_percentage')
    stud_doc = stud_ref.get()
    doc = stud_doc.to_dict()
    subwise = [v for v in doc.values()]
    subwise.pop(-1)
    data = {
        'stud_id':stud_id,
        'subwise':subwise
    }
    return data
    # function ended

def get_sub_studwise_datewise(dept,date,sub_id):
    # [Function to get subject's studentwise attendance on particular date]
    db = firestore.Client()
    sub_ref = db.collection('Students').document(dept+'/Attendance/'+date).get().to_dict()
    return sub_ref[sub_id]
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







