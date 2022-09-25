while true; do
	source /home/michael/FB-Folder/farmbox/code/drivers/tensorflow/tensor-venv/bin/activate
	python3 drivers/tensorflow/predict.py
	deactivate
	python3 drivers/tensorflow/write-to-fs.py
	sleep 86400
# sleep for 86400 seconds, one day
done
