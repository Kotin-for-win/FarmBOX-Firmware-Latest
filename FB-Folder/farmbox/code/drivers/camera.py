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

import cv2
from time import sleep
cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
if cap.isOpened():
	print("open")
	while True:
		print("true")
		sleep(0.75)
		ret, frame = cap.read()
		cv2.imwrite('/home/michael/FB-Folder/streams/class0/stream.jpg', frame)
