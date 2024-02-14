# Anti-gravity finger

**Description:** Project aiming to counter the effect of gravity on a one-degree of liberty arm (i.e finger) by programming a torque control command on Dynamixel motor.

![demo](https://raw.githubusercontent.com/Julienchh/antigravity-arm/master/assets/demo.gif)

[👨‍💻 Developer documentation](docs/developer) • [📈 Project report](docs/report) • [📚 Bibliography](docs/bibliography)
  
## 📄 This project in short

In this project, you will find a **Python module** that allows you to control your **Dynamixel motor** with **torque commands**.


* One degree of freedom available ;
* Countering of friction based on Stribeck model ;
* Use of pypot library ;
* Constants available for Dynamixel MX-64 and Dynamixel MX-106 (code is available to determine constants for other models).

## 🚀 Quickstart 

### **Install instructions**:

* Clone this repo
```bash
git clone https://github.com/Julienchh/antigravity-arm
```


* Create a conda environment with all the dependencies:
```bash
conda create -n antigravity-arm
pip3 install numpy scipy matplotlib pypot
```


### **Launch instructions**: Few lines of code to launch the main feature of your project

* Connect your Dynamixel motor to your computer (don't forget to plug the power supply). Check the name of the device (often *ttyACMx* or *ttyUSBx*) with the following command:

```bash
$ ls /dev/tty*
... /dev/ttyS3   /dev/ttyS8
/dev/tty12  /dev/tty19  /dev/tty25  /dev/tty31  /dev/tty38  /dev/tty44  /dev/tty50  /dev/tty57  /dev/tty63  /dev/ttyS11  /dev/ttyS18  /dev/ttyS24  /dev/ttyS30  /dev/ttyS9
/dev/tty13  /dev/tty2   /dev/tty26  /dev/tty32  /dev/tty39  /dev/tty45  /dev/tty51  /dev/tty58  /dev/tty7   /dev/ttyS12  /dev/ttyS19  /dev/ttyS25  /dev/ttyS31  /dev/ttyUSB0 # here, it is the last one 
```
* Activate your conda environment :
```bash
conda activate antigravity-arm
```
* Find your motor's ID with:
```bash
$ python3 -c "import pypot.dynamixel; dxl_io = pypot.dynamixel.Dxl320IO('/dev/ttyUSB0'); print(dxl_io.scan())"
>>> [20]
```
* In the file `src/compensation.py`, change the following information according to your setup:

```python
DXL_ID = 20             # found just above
PORT = "/dev/ttyUSB0"   # found with the ls command 
MASS = 0.08             # Object mass attached to motor (in kg)
DISTANCE = 0.25         # Center of mass of the object attacher to motor
OFFSET = 90.            # Offset in degrees : the angle value when the object attached to the motor is pointing downwards (minimal torque value)
```

* Launch the program and enjoy the anti-gravity finger !

```bash
python3 src/compensation.py
```

## 🔍 About this project

|       |        |
|:----------------------------:|:-----------------------------------------------------------------------:|
| 💼 **Client**                |  [Pollen Robotics](https://www.pollen-robotics.com/)                                              |
| 🔒 **Confidentiality**       | **Public**                                          |
| ⚖️ **License**               |  GNU GPLv3                  |
| 👨‍👨‍👦 **Authors**               |  [Matteo Caravati](https://www.linkedin.com/in/mcaravati/), Julien Chabrier, [Nicolas Gry](https://www.linkedin.com/in/nicolas-gry/)    |


## ✔️ Additional advices

* Do not make **passwords** and secret keys public. If you have to, replace it by a random string and a warning in the doc telling to replace it
* Avoid **long sentences**. Often, bullet points are easier to read
* **Illustrate** your reports. Use colored plots, schematics and pictures. But do not abuse of them
* Do not **duplicate** information. If it may be relevant at several places, make links
* **English** is the universal langage worldwide. Write all engineering documents in English
* Choose carefully **what sections** apply to your project and delete/add anything from the template that you think relevant
* Remove anything that would **pollute** reading, including these instructions and irrelevant sections
