# AI-Trash-Detection-Sorting-Project


Raspberry Pi 4B AI Recycling Sorter — Setup and User Guide
This guide explains how to set up and operate the camera-based recycling detector with red and green LEDs on a Raspberry Pi 4 Model B. It documents the companion Python program camera_yolo.py without reproducing its source code.
1. What the project does
The Raspberry Pi camera captures live images. An Ultralytics YOLO11n model, exported to the NCNN format for Raspberry Pi, detects a limited selection of objects. The program labels them and controls two LEDs:
Detected object
On-screen result
Green LED (GPIO 18)
Red LED (GPIO 17)
Bottle
POTENTIALLY RECYCLABLE
On
Off
Banana, apple, or orange
NON-RECYCLABLE
Off
On
Cup or other detected but unclassified object
UNKNOWN
Off
Off

Important: The pre-trained model recognizes objects, not their materials or actual recycling eligibility. A bottle could be plastic or glass, and local recycling rules differ. Food scraps may belong in compost rather than landfill. This is a demonstration, not a reliable automated sorting decision.
Current code limitations: The program handles up to two detections per frame. When two objects are detected, each may change the LEDs in turn, so the last processed detection wins. When nothing is detected, the current code does not reset the LEDs, so a previously lit LED can stay on. The current cleanup closes the camera and display but does not explicitly turn off/close the LEDs. Power down or disconnect the LEDs after use if necessary; improve the script before connecting any actuator.

2. Required hardware
Raspberry Pi 4 Model B with a suitable power supply, microSD card, and Raspberry Pi OS with a graphical desktop.
Raspberry Pi-compatible CSI camera and ribbon cable.
One red LED and one green LED.
Two current-limiting resistors, typically 220–330 Ω, one per LED.
Breadboard and jumper wires.
Monitor, keyboard, and mouse for the live detection window.
LED wiring (BCM GPIO numbering)
Shut down the Pi and disconnect power before changing wires. Do not connect an LED directly across a GPIO pin and ground without a resistor.
Component
Raspberry Pi connection
Physical header pin
Red LED control
GPIO 17 (BCM)
Pin 11
Green LED control
GPIO 18 (BCM)
Pin 12
LED ground connections
Any GND pin
Pin 6 is one option

For each LED, connect its GPIO output through a 220–330 Ω resistor to the LED anode (longer leg, +), and connect the cathode (shorter leg, − / flat side) to a Raspberry Pi GND pin. Each LED needs its own resistor. Do not wire an LED to 5 V or connect a 5 V signal to a GPIO input.
GPIO Zero uses BCM GPIO numbers, not physical header pin numbers. The Python program's LED(17) and LED(18) refer to GPIO 17 and GPIO 18.

3. Set up Raspberry Pi OS and camera
Boot the Pi and connect to the internet.
Open Terminal.
Update the package list using sudo apt update.
Ensure the system packages python3-venv, python3-pip, python3-picamera2, python3-opencv, and python3-gpiozero are installed with Raspberry Pi OS's apt package manager.
Check the architecture with uname -m. The working project used aarch64 (64-bit) and Python 3.11.
Test the camera with the Raspberry Pi camera preview utility, typically rpicam-hello -t 5000 on current Raspberry Pi OS. Depending on the OS version, the older name may be libcamera-hello.
Confirm the image appears before continuing. If not, shut down the Pi and inspect the ribbon cable orientation and seating.

5. Find your saved project files
The working project used these paths:
Project folder: ~/Desktop/Python programs/
Python program: ~/Desktop/Python programs/camera_yolo.py
Exported model folder: ~/Desktop/Python programs/yolo11n_ncnn_model/
Python virtual environment: ~/yolo_env/
In Terminal, use cd ~/Desktop/"Python programs" to enter the folder. Check that the Python file and the model directory are present using ls.
Files and installed packages are saved after shutting down the Raspberry Pi. However, the virtual environment is not automatically active in a new terminal window.

7. Activate the existing Python environment (every new terminal session)
Open Terminal.
Enter source ~/yolo_env/bin/activate.
Check for (yolo_env) at the beginning of the terminal prompt.
Enter cd ~/Desktop/"Python programs".
Do this every time you restart the Pi or open a new terminal. If the terminal does not show (yolo_env), a ModuleNotFoundError for ultralytics or ncnn does not necessarily mean the packages are gone.
If activation fails because the file cannot be found, locate the original environment before creating another one.
8. Software dependencies
The current program uses:
Package / tool
Purpose
Python 3
Runs the project
OpenCV (cv2)
Displays the image and detection boxes
Picamera2
Captures frames from the Raspberry Pi camera
Ultralytics YOLO
Detects recognized objects
NCNN runtime
Runs the exported model efficiently on the Pi
GPIO Zero (gpiozero)
Controls the red and green LEDs
PyTorch / TorchVision
Used to load or export the original YOLO model; not necessarily required for inference with an already exported NCNN model
NumPy
Image arrays and library dependency

For an already working setup, do not reinstall these packages. After activating yolo_env, verify package availability using Python's import checks or python -m pip list. Check the model folder before attempting another export.
For a clean installation, use the Raspberry Pi OS system packages for Picamera2, camera libraries, and GPIO Zero, then create a Python virtual environment with system site packages enabled (so the virtual environment can access those system libraries). Install a mutually compatible Ultralytics, NCNN, PyTorch, NumPy, pandas, and OpenCV set for your Raspberry Pi OS and Python version. The original project encountered incompatibilities between NumPy 2.x and system simplejpeg; it subsequently used NumPy 1.26.4 and pandas 2.2.3. These are historical troubleshooting details, not a guarantee that the same pins will work on every OS image. Avoid blindly upgrading all dependencies after the setup works.
7. Prepare the YOLO NCNN model
Confirm the folder yolo11n_ncnn_model already exists beside camera_yolo.py.
If it exists, do not export again.
If it does not exist, first confirm that the original yolo11n.pt model and Ultralytics are available. From the project folder, export with the Ultralytics CLI command yolo export model=yolo11n.pt format=ncnn imgsz=320.
A successful export creates a directory named yolo11n_ncnn_model, typically containing metadata.yaml, model.ncnn.bin, and model.ncnn.param.
The program should reference the NCNN model directory, not the original .pt file.
The previously exported model is not embedded in this README. Anyone copying the project must also copy the model folder or export their own.
8. Run the recycling detector
Connect the camera and both LED circuits according to Section 2, with power off while wiring.
Turn on the Pi and open Terminal.
Activate the environment with source ~/yolo_env/bin/activate.
Go to the project folder with cd ~/Desktop/"Python programs".
Confirm that camera_yolo.py and yolo11n_ncnn_model/ are present.
Start the program with python camera_yolo.py.
A window named AI Recycling Sorter should show a live image with detected objects, labels, and colored bounding boxes.
Place one item at a time under the camera, on a simple, uncluttered background. The single-item method avoids conflicting LED commands when two detections are present.
Observe the screen label and LEDs. A bottle should light the green LED; a detected banana, apple, or orange should light the red LED; an unknown detected object should turn both off.
Because the current code can leave the last LED on when no object is detected, do not interpret a lit LED as proof that an object is currently present.
Detection settings in the current script
Setting
Current value
Effect
Camera size
640 × 480
Live camera image
Model input size
320 pixels
NCNN inference input size
Confidence threshold
0.80
Filters lower-confidence predictions
IoU threshold
0.30
Suppresses overlapping detections
Maximum detections
2 per frame
Limits displayed predictions
COCO class IDs
39, 41, 46, 47, 49
Bottle, cup, banana, apple, orange

Only the above five general-purpose COCO classes are requested. The stock model does not recognize all kinds of paper, cardboard, cans, wrappers, or recycling contamination. To sort those correctly, a custom-trained recycling dataset/model is required.
9. How to stop the program safely
Click the video window and press Q; or
Click the terminal and press Ctrl+C.
The current script stops the camera and closes the OpenCV windows. It does not explicitly call off() or close() on either LED during cleanup; a light may remain in its most recent state until the process ends or GPIO state changes. Verify the LEDs are off before leaving the setup unattended.
10. Common troubleshooting
ModuleNotFoundError: No module named 'ultralytics' or 'ncnn'
Usually means the virtual environment is not active after reboot. Activate ~/yolo_env and verify (yolo_env) appears at the terminal prompt. Do not immediately reinstall everything.
externally-managed-environment during package installation
This usually means pip is being run outside the virtual environment on Raspberry Pi OS. Activate yolo_env, then use the environment's python -m pip. Do not use --break-system-packages just to bypass the warning.
ValueError: numpy.dtype size changed
The NumPy version may not be binary-compatible with the system-provided camera/`simplejpeg` package. In the original setup, NumPy 2.1.1 triggered this error, and NumPy 1.26.4 was installed; pandas 3.x then required a different NumPy range and was replaced with pandas 2.2.3. Resolve package compatibility deliberately rather than repeatedly upgrading packages.
Illegal instruction during inference or export
A compiled package may use processor instructions unsupported by Raspberry Pi 4B. Test the model without the camera to isolate the issue. The original project required a compatible PyTorch/Ultralytics combination before the NCNN export succeeded. If the NCNN model is already exported and works, avoid rebuilding it unnecessarily.
Hundreds of boxes or nonsensical objects with confidence 1.00
This occurred in the original setup. It indicates a likely model-export, runtime, or output-decoding problem; raising confidence or limiting detections only reduces clutter. Test the model on a known image before trusting classifications or connecting a sorting servo. Never allow unverified model output to actuate hardware.
LEDs not lighting
Recheck GPIO 17 and 18 in BCM numbering versus physical pins 11 and 12.
Check the LED polarity (anode +, cathode −), ground connection, and individual series resistors.
Verify GPIO Zero is available in the activated environment.
Remember that red and green outputs are intentionally off when the current detection is UNKNOWN.
If nothing is detected, the current code does not automatically reset an LED that was previously on.
LED shows the wrong result when two objects appear
The current script updates the LEDs separately for each bounding box. With two detections, the final detection processed controls the LEDs. For reliable behavior, place one item at a time under the camera, or modify the program to choose a single target or aggregate the detection results per frame.
11. Known limitations and next improvements
Add explicit both-LEDs-off at the beginning of each frame and in the finally cleanup section.
Decide what should happen if two different objects are seen at the same time (for example, choose the one nearest the belt center).
Add several consecutive agreeing frames before changing an LED or moving a servo to reduce false triggers.
Train a recycling-specific YOLO model for plastic bottles, aluminum cans, cardboard, paper, wrappers, and other actual project materials, then export it to NCNN.
Check recycling eligibility against local waste rules; food scraps may need their own compost category.
If a conveyor or servo flap is later connected, add a safe unknown/no-sort behavior and a physical stop mechanism. Do not drive a servo based on the current demonstration labels.
12. References
Raspberry Pi camera software: https://www.raspberrypi.com/documentation/computers/camera_software.html
Picamera2 manual and examples: https://github.com/raspberrypi/picamera2
GPIO Zero documentation: https://gpiozero.readthedocs.io/
Ultralytics Raspberry Pi guide: https://docs.ultralytics.com/guides/raspberry-pi/
Ultralytics NCNN export: https://docs.ultralytics.com/integrations/ncnn/

Sharing this project: Provide the recipient with this README, your separate camera_yolo.py file, and the exported yolo11n_ncnn_model/ directory. The README intentionally contains instructions only and no complete Python source code.


