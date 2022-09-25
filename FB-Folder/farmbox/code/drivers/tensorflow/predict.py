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

import tensorflow as tf
import numpy as np
import scipy
import os
from tensorflow import keras
from os.path import exists

class OpenFiles():
    def __init__(self):
        self.files = []
    def open(self, file_name, otype):
        f = open(file_name, otype)
        self.files.append(f)
        return f
    def close(self):
        list(map(lambda f: f.close(), self.files))
files=OpenFiles()

planttypesource = files.open("/home/michael/FB-Folder/farmbox/data/plantType.txt", 'r')
plantType = planttypesource.readline().strip('\n')
if os.path.exists("/home/michael/FB-Folder/CustomModels/ActualModels/" + plantType + "-ripe" + ".h5"):
	reloaded = tf.keras.models.load_model("/home/michael/FB-Folder/CustomModels/ActualModels/" + plantType + "-ripe" + ".h5")
else:
	reloaded = tf.keras.models.load_model("/home/michael/FB-Folder/farmbox/code/drivers/tensorflow/" + plantType + "-ripe" + ".h5")
from tensorflow.keras.preprocessing.image import ImageDataGenerator

image_gen_test = ImageDataGenerator(rescale=1. / 255)
test_data_gen = image_gen_test.flow_from_directory(batch_size=10,
                                                   directory="/home/michael/FB-Folder/streams/",
                                                   shuffle=True, target_size=(150, 150), class_mode='binary')
predicted_batch = reloaded.predict(test_data_gen)
predicted_batch = tf.squeeze(predicted_batch).numpy()
predicted_ids = np.argmax(predicted_batch, axis=-1)

print("Ripeness: ", predicted_ids)
with files.open(r'/home/michael/FB-Folder/farmbox/data/ai-ripe.txt', 'w') as ripe_txt:
	ripe_txt.write(str(predicted_ids))
	
if os.path.exists("/home/michael/FB-Folder/CustomModels/ActualModels/" + plantType + "-sick" + ".h5"):
	reloaded = tf.keras.models.load_model("/home/michael/FB-Folder/CustomModels/ActualModels/" + plantType + "-sick" + ".h5")
else:
	reloaded = tf.keras.models.load_model("/home/michael/FB-Folder/farmbox/code/drivers/tensorflow/" + plantType + "-sick" + ".h5")
from tensorflow.keras.preprocessing.image import ImageDataGenerator

image_gen_test = ImageDataGenerator(rescale=1. / 255)
test_data_gen = image_gen_test.flow_from_directory(batch_size=10,
                                                   directory="/home/michael/FB-Folder/streams/",
                                                   shuffle=True, target_size=(150, 150), class_mode='binary')
predicted_batch = reloaded.predict(test_data_gen)
predicted_batch = tf.squeeze(predicted_batch).numpy()
predicted_ids = np.argmax(predicted_batch, axis=-1)

print("Sickness: ", predicted_ids)
with files.open(r'/home/michael/FB-Folder/farmbox/data/ai-sick.txt', 'w') as ripe_txt:
	ripe_txt.write(str(predicted_ids))
files.close()
