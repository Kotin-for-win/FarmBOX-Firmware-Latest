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
import os
import time
import serial
from firebase_admin import credentials
from firebase_admin import firestore

#File manager library to ensure locks aren't kept
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

# Handle syncing data with Firestore
cred = credentials.Certificate('/home/michael/FB-Folder/farmbox/serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
uuid = files.open(r'/home/michael/FB-Folder/farmbox/data/UUID.txt', 'r').readline().strip('\n')

doc_ref = db.collection(u'farmboxes').document(uuid)
if files.open(r'/home/michael/FB-Folder/farmbox/data/ai-ripe.txt', 'r').readline().strip('\n') == "0":
	ripeness = "yes"
else:
	ripeness = "no"
sick_file = files.open(r'/home/michael/FB-Folder/farmbox/data/ai-sick.txt', 'r').readline().strip('\n')
planttypesource = files.open("/home/michael/FB-Folder/farmbox/data/plantType.txt", 'r')
plantType = planttypesource.readline().strip('\n')
if sick_file == "":
	sickness = "no"
else:
	try:
		sick_keymap = files.open(r'/home/michael/FB-Folder/CustomModels/KeyMaps/' + plantType + '-sick.txt', 'r').readlines()
		sickness = sick_keymap[int(sick_file)].strip('\n')
	except IOError:
		print("Handle TF, keymap not found, continuing anyway...")
		sickness = "no"
doc_ref.set({
   u'new-ai': True,
   u'ai-ripe': ripeness,
   u'ai-health': sickness
}, merge=True)
files.close()

#serial port communication for Wio
serialPort = "/dev/ttyACM0" #this is the serial port the wio always gets assigned, we tested!
baudRate = 115200
ser = serial.Serial(serialPort, baudRate, timeout=0.5)
serRipe = ser.write(str.encode(ripeness))
serSick = ser.write(str.encode(sickness))
