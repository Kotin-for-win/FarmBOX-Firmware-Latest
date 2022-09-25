# FarmBOX Firmware - code for the Raspberry Pi inside a FarmBOX
# Copyright (C) 2022 Michael Reeves

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading
import os 
from time import sleep

class OpenFiles():
    def __init__(self):
        self.files = []
    def open(self, file_name, otype):
        f = open(file_name, otype)
        self.files.append(f)
        return f
    def close(self):
        list(map(lambda f: f.close(), self.files))
files = OpenFiles()

cred = credentials.Certificate('/home/michael/FB-Folder/farmbox/serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
uuid = files.open(r'/home/michael/FB-Folder/farmbox/data/UUID.txt', 'r').readline().strip('\n')
def refresh():
    print("Here we go again! [Update Firestore Data]")
    doc_ref = db.collection(u'farmboxes').document(uuid)
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        print(f'Document data: {data}')
        init = data[u'init']
        if str(init) == "2":
                if u"interval" in data:
                   interval = data[u'interval']
                   with files.open(r'/home/michael/FB-Folder/farmbox/data/interval.txt', 'w') as data2:
                      data2.write(str(interval))
                else:
                   print("No Interval, continuing...")
                if u"wt" in data:
                   wt = data[u'wt']
                   #water thershold
                   with files.open(r'/home/michael/FB-Folder/farmbox/data/wt.txt', 'w') as data3:
                      data3.write(str(wt))
                else:
                   print("No wt, continuing...")
                if u"bt" in data:
                   bt = data[u'bt']
                   #bar threshold
                   with files.open(r'/home/michael/FB-Folder/farmbox/data/bt.txt', 'w') as data4:
                      data4.write(str(bt))
                else:
                   print("No bt, continuing...")
                if u"length" in data:
                   length = data[u'length']
                   with files.open(r'/home/michael/FB-Folder/farmbox/data/length.txt', 'w') as data5:
                      data5.write(str(length))
                else:
                   print("No length, continuing...")
                if u"plant-type" in data:
                   ptype = data[u'plant-type']
                   with files.open(r'/home/michael/FB-Folder/farmbox/data/plantType.txt', 'w') as data65:
                      data65.write(str(ptype))
                else:
                   print("No plant-type, continuing...")
                if u"wifi" in data:
                   wifi = data[u'wifi']
                   if wifi == True:
                   	print("WiFi selected by user")
                   	ssid = data[u'wifi-ssid']
                   	pword = data[u'wifi-pword']
                   	os.system("nmcli d wifi connect " + ssid + " password " + pword)
                   elif wifi != None:
                   	print("User wants helium")
                else:
                   print("No wifi, and done!")
                files.close()
                sleep(900)
                #15 minutes
                refresh()
       	else:
       	        print("unknown bug")
       	        files.close()
       	        sleep(900)
       	        #15 minutes
       	        refresh()
       	        

    else:
     print(u'No such document!')
     files.close()
     sleep(900)
     #15 minutes

refresh()


