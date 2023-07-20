# Ball Speed Measurement Program

This is the technical documentation for the "Ball Speed Measurement" program written in Python. The program is designed to recognize balls in a video, measure their speed before and after a collision, and display the results in real-time. The program uses the OpenCV library for image processing, PyQt5 for the user interface, and matplotlib for data visualization.

## Requirements
- Python 3.x
- OpenCV
- NumPy
- Matplotlib
- PyQt5

## Installation
1. Make sure you have Python 3.x installed on your system.
2. Install the required libraries using the following command:
   ```
   pip install opencv-python numpy matplotlib PyQt5
   ```

## Usage
1. Clone or download the repository from GitHub.
2. Open the terminal or command prompt and navigate to the program's directory.
3. Run the program using the following command:
   ```
   python main.py
   ```
4. The application window will open, showing the video feed and the measured ball speeds.

## Program Description

The program consists of two main classes:

### 1. PetangBall Class
This class represents a petang ball and handles its speed calculations.

#### Attributes
- `radius`: The radius of the petang ball.
- `prev_position`: The previous position of the petang ball.
- `object_diameter`: The assumed diameter of the petang ball in pixels.
- `object_real_size`: The actual size of the petang ball in meters.
- `pixel_to_meter`: Conversion factor from pixels to meters.
- `speed`: The current speed of the petang ball in meters per second.
- `speed_pixels_x`: The current speed of the petang ball in the x-axis in pixels per second.
- `speed_pixels_y`: The current speed of the petang ball in the y-axis in pixels per second.
- `speed_meters_x`: The current speed of the petang ball in the x-axis in meters per second.
- `speed_meters_y`: The current speed of the petang ball in the y-axis in meters per second.
- `max_speed`: The maximum speed recorded for the petang ball.
- `speed_array`: An array to store the speed values over time.
- `time_array`: An array to store the corresponding time values.

#### Methods
- `move`: Calculate the speed of the ball based on the change in position and elapsed time.
- `includes`: Check if the petang ball includes another ball (used to detect collisions).
- `label_text`: Return the speed information as a list of strings for display.

### 2. PetangStorage Class
This class is used to store and manage multiple petang balls.

#### Attributes
- `objects`: A list of PetangBall objects representing the detected balls.
- `last_petan`: The last detected petang ball (used to compare and track changes).
- `last_frame`: The timestamp of the last frame processed.

#### Methods
- `update_contours`: Update the ball positions and speeds based on the detected contours in the current frame.
- `draw_arrows`: Draw arrows representing the ball's speed direction on the frame.
- `draw_labels`: Draw speed labels on the frame.

### 3. SpeedMeasurementApp Class
This class is responsible for the user interface and video processing.

#### Attributes
- `speed_array`: An array to store the ball speeds over time.
- `time_array`: An array to store the corresponding time values.
- `min_radius`: Minimum radius of a ball to be considered.
- `max_radius`: Maximum radius of a ball to be considered.
- `timer_ticks`: Interval for frame processing (in milliseconds).
- `storage`: An instance of the PetangStorage class for managing petang balls.

#### Methods
- `init`: Initialize the user interface and setup camera parameters.
- `setup_ui`: Create the main application window and buttons.
- `plot_speed_graph`: Plot the ball speed graph using Matplotlib.
- `setup_camera`: Open the video capture and set up the QTimer for frame processing.
- `find_black_circles`: Find black circles in the frame (used for collision detection).
- `find_petan_circles`: Find petang balls in the frame using color segmentation.
- `find_ball_circles`: Find the balls that meet the specified radius criteria.
- `crop_frame`: Crop the frame to the specified dimensions.
- `update_frame`: Process the frames, detect balls, and update the display.
- `start_measurement`: Start the speed measurement.
- `reset_measurement`: Reset the video capture and measurement data.
- `resetspeed_measurement`: Reset the speed measurement data.
- `pause_measurement`: Pause or resume the speed measurement.
- `closeEvent`: Handle the event when the application is closed, releasing the video capture and displaying the speed graph.

## Limitations and Improvements
- The program's accuracy might be affected by various factors such as lighting conditions, ball surface, and camera quality.
- The program assumes that there are only two types of balls (black and petang) and may not work well with different ball types.
- To improve accuracy, you can calibrate the program using known ball speeds and sizes.
- The user interface could be enhanced to provide more features and options, such as selecting video files, adjusting settings, and exporting data.

Note: This documentation assumes basic familiarity with Python, OpenCV, and PyQt5. If you encounter any issues or have questions about the program, please refer to the source code and feel free to ask for further assistance.