echo "Installing FarmBOX Firmware... [Install Script v1.0]"
if [ $(whoami) == "root" ]; then
	echo "You are root. Continuing..."
	echo "Stage [1/9]: Configuring network..."
	hostnamectl set-hostname $1
	dhclient eth0
	apt update
	apt -y upgrade
	apt -y install network-manager
	systemctl start network-manager
	apt -y install git
	echo "Stage [2/9]: Configuring Filesystem..."
	mkdir /home/michael
	mkdir /home/michael/FB-Folder
	cp -r FB-Folder /home/michael/FB-Folder
	mkdir /home/michael/FB-Folder/CustomModels
	mkdir /home/michael/FB-Folder/CustomModels/ActualModels
	mkdir /home/michael/FB-Folder/CustomModels/KeyMaps
	mkdir /home/michael/FB-Folder/streams
	mkdir /home/michael/FB-Folder/streams/class0
	mkdir /home/michael/FB-Folder/streams/class1
	pathToSA=$(find /media/* -name "serviceAccount.json"
	cp $pathToSA /home/michael/FB-Folder/FB-Folder
	echo "Stage [3/9]: Installing APT Packages"
	apt -y install python3 python3-dev python3-pip build-essential libssl-dev libffi-dev python-dev python3-venv nano
	apt -y install raspi-config lua5.1 libatopology2 libfftw3-single3 libsamplerate0 alsa-utils
	echo "Stage [4/9]: Configuring NGINX..."
	cp nginx.conf /etc/nginx
	echo "Stage [5/9]: Installing system-wide PIP Packages..."
	python3 -m pip install firebase_admin piicodev lgpio
	python3 -m pip install -r FB-Folder/requirements-normal.txt
	echo "Stage [6/9]: Setting up TensorFlow Virtual Python Enviornment..."
	python3 -m venv /home/michael/FB-Folder/farmbox/code/drivers/tensorflow/tensor-venv
	source /home/michael/FB-Folder/farmbox/code/drivers/tensorflow/tensor-venv/bin/activate
	pip install -r FB-Folder/requirements-venv.txt
	deactivate
	echo "Stage [7/9]: Activating FarmBOX Security Policy..."
	chown -r root /home/michael/FB-Folder
	chmod -r 700 /home/michael/FB-Folder/farmbox
	chmod -r 700 /home/michael/FB-Folder/fb-upgrade
	chmod -r 777 /home/michael/FB-Folder/CustomModels
	chmod -r 777 /home/michael/FB-Folder/streams
	echo "Stage [8/9]: Configuring bootloader..."
	notedDir=$(df -h | grep /boot/firmware | awk '{print $1}')
	mount $notedDir /boot
	echo "Stage [9/9]: Configuring crontab..."
	crontab -l -u root | cat - tabby.txt | crontab -u root -
	echo "Script run finished OK. Please refer to documentation to continue setup."
else
	echo "FATAL: Not root. Please refer to documentation."
fi

