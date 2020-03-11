from datetime import datetime as date
sub = 4
slot = 4
daylist = {'Monday':{
	'slot0': 'sub0',
	'slot1': 'sub1',
	'slot2': 'sub2',
	'slot3': 'sub3',
},
'Tuesday' : {
	'slot0': 'sub0',
	'slot1': 'sub1',
	'slot2': 'sub2',
	'slot3': 'sub3',
},
'Wednesday' : {
	'slot0': 'sub0',
	'slot1': 'sub1',
	'slot2': 'sub2',
	'slot3': 'sub3',
},

'Thursday' : {
	'slot0': 'sub0',
	'slot1': 'sub1',
	'slot2': 'sub2',
	'slot3': 'sub3',
},

'Friday' : {
	'slot0': 'sub0',
	'slot1': 'sub1',
	'slot2': 'sub2',
	'slot3': 'sub3',
},

'Saturday' : {
	'slot0': 'sub0',
	'slot1': 'sub1',
	'slot2': 'sub2',
	'slot3': 'sub3',
}}
def return_daydata(today):

	return daylist[today]

# print(date.today().strftime("%A"))