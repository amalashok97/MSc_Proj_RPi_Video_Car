# Installation of the qr_tracker as a ros package
Must login as root to run the following: 

sudo su

## User profile
Update the user profile to add this line 

```sh
export WORKON_HOME=/home/<user>/.virtualenvs
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
source /home/<user>/ros_catkin_ws/devel/setup.bash
```

run source to enable the commands - you will need to do this every time if you do not login as root

```sh
source /root/.profile
```

## Python dependences
Run the following commands to complete installation of dependencies in virtual environment

```sh 
workon cv
pip install python-dev python-setuptools
apt-get install python-pil
pip install http://effbot.org/downloads/Imaging-1.1.6.tar.gz
pip install catkin_pkg
pip install netifaces
pip install smbus
apt-get install libzbar-dev //This might not be needed 
apt-get install libiconv-hook-dev
apt-get install libffi-dev libffi6 libzbar-dev
pip install libzbar-cffi
pip install tesseract-ocr
pip install pytesseract
```

if you want to run ocr tests also install
tesserocr - https://github.com/sirfz/tesserocr
and 
pyocr - https://github.com/openpaperwork/pyocr

## Preparation of the ros package
Clone the disto-robots repo

```sh
git clone <address to distro-robots-repo>
mkdir -r qr_tracker/include/qr_tracker
```

Copy the code into ros

```sh
cp -rf qr_tracker/  <path to ros catkin workspace>/src/.
```

## Adjust the IPs and paths in the source code
On all the files below you will need to change the paths and IPs as they are hard-coded into the source files

### Run the initial tests
This is to make sure that all paths and IPs are correct and to make sure that the ros package will be built on the latest and working version of the code 

Test that the motor is working 
```sh
./testmotor.oy
```
This should make the car move it's front wheels left and right 

If you have the correct server IP setup in camtest.py, test that cam is working
```sh 
./camtest.py
```
This should start a server that displays the camera stream and you can see this in a browser at: 
* http://<robot_IP>:8080/stream.html


### Build the ros package
Build the qr_tracker ros package in the catkin workshpace 
```sh
cd <path to catkin workshpace>
catkin_make --pkg qr_tracker
```
Then launch the ros node
```sh
roscd qr_tracker/src
roslaunch qr_tracker.launch
```