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

print("Commander Service Started!")
print("Checking setupState...")

import os
import shlex
from subprocess import Popen


os.system("systemctl start nginx")
os.system("cd /home/michael/FB-Folder/farmbox/code")
def checkSetup():
	setupState = open("/home/michael/FB-Folder/farmbox/data/setupState.txt").readline().strip('\n')
	print("setupState is " + setupState)
	if setupState == "none":
		print("No setup done!")
		os.system("python3 /home/michael/FB-Folder/farmbox/code/setup/initalisation.py")
		checkSetup()
	if setupState == "unassigned":
		print("Basic Setup done, but we have no mobie device.")
		os.system("python3 /home/michael/FB-Folder/farmbox/code/setup/wait_for_pair.py")
		checkSetup()
	if setupState == "setup-done":
		print("All setup done!")
		tf_enviro = Popen(['/bin/bash', 'tf-manager.sh'])
		#sensor_enviro = Popen(['/bin/bash', 'sensor-manager.sh'])
		camera_enviro = Popen(['/bin/bash', 'camera-manager.sh'])
		water_enviro = Popen(['/bin/bash', 'water_manager.sh'])
		refresh_enviro = Popen(['/bin/bash', 'refresh_manager.sh'])
		update_enviro = Popen(['/bin/bash', 'upgrade_manager.sh'])
		checkSetup()
checkSetup()

#!/bin/bash

#echo "FarmBOX Commander Service V1.0 Started!"
#echo "Verifying setupState..."

#setupState=$(cat /home/michael/FB-Folder/farmbox/data/setupState.txt)

#if [ $setupState == "none" ]; then
#echo "No Setup has been completed. Calling init routine..."
#python3 /home/michael/FB-Folder/farmbox/code/setup/initalisation.py
#sudo systemctl restart FarmBOX-Commander
#else
#echo "Something's wrong"
 #   fi
#if [ $setupState == "unassigned" ]; then
#    echo "Basic setup has completed, but a mobile device has not paired with us."
 #   python3 /home/michael/FB-Folder/farmbox/code/setup/wait_for_pair.py
  #  sudo systemctl restart FarmBOX-Commander
   # fi
#if [ $setupState == "setup-done" ] ; then
#	echo "All setup has been completed."
 #   	echo "Subscrbing for realtime updates..."
  #  	sudo systemctl start FarmBOX-subscriber
#	echo "Starting Evaluation Service..."
#    	sudo systemctl start FarmBox-eval
 #   	echo "Done!"
#	fi
