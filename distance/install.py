"""
This script installs the required packages for the YOLOv5 model.

It uses pip to install the packages listed in the requirements.txt file.
"""
from subprocess import Popen
comand=['pip', 'install', '-r' "code/yolo5/requirements.txt"]
Popen(comand)