import os
import identify_face_img as ifi
import cloud_to_pc as cp
import dbase
from datetime import datetime as date
# import testauto as ta
# today_day = date.today().strftime("%A")
# today_data = ta.return_daydata(today_day)
count = 0
while True:

    cp.download_to_local()
    file_name = os.listdir("face_img")
    #print(file_name)
    pt = {}
    #print(pt)

    if len(file_name) != 0:
        pt['sub_id'] = "sub_"+str(count)
        for i in file_name:
            path = "face_img" + "//" + i
            name = ifi.face_rec(path)
        name = list(set(name))
        pt['sub_arr'] = name
        count += 1
        dbase.update_attendance(pt)
    if len(pt) != 0:
        print(pt)
    if len(file_name) != 0:
        for i in file_name:
            path = "face_img" + "//" + i
            os.remove(path)




