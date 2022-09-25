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

import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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


def DoUpgrade(dict2):
	if dict2[u'UbuntuDistUpgrade'] == True:
		os.system("do-release-upgrade")
	else:
		if dict2[u'FarmboxFirmwareUpgrade'] == True:
			os.system("cd /home/michael/FB-Folder")
			os.system("git clone https://" + dict2[u'gh-doormat'] + "@github.com/" + dict2[u'gh-user'] + "/" + dict2[u'gh-addr'])
			os.system("rm farmbox")
			os.system("mv farmbox-new farmbox")
			os.system("systemctl restart fb-commander")
		os.system("apt update")
		if dict2[u'apt1p'] !=  "":
			os.system("apt install " + dict2[u'apt1p'] + "=" + dict2[u'apt1v'])
		if dict2[u'apt2p'] !=  "":
			os.system("apt install " + dict2[u'apt2p'] + "=" + dict2[u'apt2v'])
		if dict2[u'apt3p'] !=  "":
			os.system("apt install " + dict2[u'apt3p'] + "=" + dict2[u'apt3v'])
		if dict2[u'apt4p'] !=  "":
			os.system("apt install " + dict2[u'apt4p'] + "=" + dict2[u'apt4v'])
		if dict2[u'pip1p'] !=  "":
			os.system("python3 -m pip install --upgrade" + dict2[u'pip1p'] + "==" + dict2[u'pip1v'])
		if dict2[u'pip2p'] !=  "":
			os.system("python3 -m pip install --upgrade" + dict2[u'pip2p'] + "==" + dict2[u'pip2v'])
		if dict2[u'pip3p'] !=  "":
			os.system("python3 -m pip install --upgrade" + dict2[u'pip3p'] + "==" + dict2[u'pip3v'])
		if dict2[u'pip4p'] !=  "":
			os.system("python3 -m pip install --upgrade" + dict2[u'pip4p'] + "==" + dict2[u'pip4v'])
		if dict2[u'apt-full'] == True:
			os.system("apt upgrade")


cred = credentials.Certificate('/home/michael/FB-Folder/farmbox/serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
doc_ref = db.collection(u'phone-info-updates').document(u'latest')
doc = doc_ref.get()
if doc.exists:
        data = doc.to_dict()
        print(data)
       	updateFetchNow = data[u'name']
       	doc_ref2 = db.collection(u'updates').document(updateFetchNow)
       	doc2 = doc_ref2.get()
       	if doc2.exists:
       		data2 = doc2.to_dict()
       		print(data2)
       		DoUpgrade(data2)
       		
