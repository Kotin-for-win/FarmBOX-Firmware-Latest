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

# Use a service account
cred = credentials.Certificate('/home/michael/FB-Folder/farmbox/serviceAccount.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

uuid = open(r'/home/michael/FB-Folder/farmbox/data/UUID.txt').readline().strip('\n')

doc_ref = db.collection(u'farmboxes').document(uuid)
doc_ref.set({
    u'init': 1
})
with open('/home/michael/FB-Folder/farmbox/data/setupState.txt', 'w') as data:
    data.write("unassigned")
    data.close()

