# Ball Speed Measurement Program

This is the technical documentation for the "Ball Speed Measurement" program written in Python. This Python program captures video from a camera, detects and tracks circular objects (balls) in the video frames, and calculates their speeds in real-time. It uses OpenCV and PyQt5 for the graphical user interface.
## Requirements
- Python 3.x
- OpenCV
- NumPy
- Matplotlib
- PyQt5

## Usage:
1. Install the required libraries listed in the requirements.txt file.
 
   ```pip install -r requirements.txt```
3. Run the Python script (main.py).
4. The application will display the video feed with detected ball speeds and arrows indicating motion direction.
5. You can pause and resume the measurement by clicking the "Pause" button.
6. Click the "Reset Speed" button to reset the speed measurements.

## Program Description

The "Ball Speed Measurement Program" is a Python program designed to capture video from a camera, detect and track circular objects (balls) in the video frames, and calculate their speeds in real-time. This application utilizes the following libraries and packages:

1. OpenCV (opencv-python): OpenCV is used for computer vision tasks, including video capture, image processing, and contour detection.

2. NumPy: NumPy is used for numerical operations and array manipulation, crucial for mathematical calculations in this application.

3. PyQt5: PyQt5 is used to create the GUI for the application, allowing users to interact with the video feed and control measurements.

4. Matplotlib: Matplotlib is used for generating graphs and charts to visualize the speed measurements over time.


## Limitations and Improvements
- The program's accuracy might be affected by various factors such as lighting conditions, ball surface, and camera quality.

Note: This documentation assumes basic familiarity with Python, OpenCV, and PyQt5. If you encounter any issues or have questions about the program, please refer to the source code and feel free to ask for further assistance.
