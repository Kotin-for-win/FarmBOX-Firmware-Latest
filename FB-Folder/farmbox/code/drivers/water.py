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

from time import sleep
import lgpio
from datetime import datetime
import os

class OpenFiles():
    def __init__(self):
        self.files = []
    def open(self, file_name):
        f = open(file_name)
        self.files.append(f)
        return f
    def close(self):
        list(map(lambda f: f.close(), self.files))

files = OpenFiles()


def water():
	MotorEPin = 16
	MotorAPin = 22
	MotorBPin = 18
	handleE = lgpio.gpiochip_open(0)
	handleA = lgpio.gpiochip_open(0)
	handleB = lgpio.gpiochip_open(0)
	lgpio.gpio_claim_output(handleE, MotorEPin)
	lgpio.gpio_claim_output(handleA, MotorAPin)
	lgpio.gpio_claim_output(handleB, MotorBPin)
	lgpio.gpio_write(handleA, MotorAPin, 1)
	lgpio.gpio_write(handleB, MotorBPin, 0)
	lgpio.gpio_write(handleE, MotorEPin, 1)
	sleep(int(files.open(r'/home/michael/FB-Folder/farmbox/data/length.txt').readline().strip('\n')))
	lgpio.gpio_write(handleE, MotorEPin, 0)
	lgpio.gpio_write(handleA, MotorAPin, 0)
	lgpio.gpiochip_close(handleE)
	lgpio.gpiochip_close(handleA)
	lgpio.gpiochip_close(handleB)
	
def wait():
	interval = int(files.open("/home/michael/FB-Folder/farmbox/data/interval.txt").readline().strip('\n'))
	files.close()
	sleep(interval)
while True:
	if int(files.open("/home/michael/FB-Folder/farmbox/data/bar.txt").readline().strip('\n')) <= int(files.open("/home/michael/FB-Folder/farmbox/data/bt.txt").readline().strip('\n')):
		wait()
	if int(files.open("/home/michael/FB-Folder/farmbox/data/temp.txt").readline().strip('\n')) >= int(files.open("/home/michael/FB-Folder/farmbox/data/wt.txt").readline().strip('\n')):
		water()
	water()
	files.close()
	wait()

	
	

