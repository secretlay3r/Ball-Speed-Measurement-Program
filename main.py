import cv2
import numpy as np
import math
import time
import sys
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib import pyplot as plt
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog



petan_radius = 37
black_radius = 90
petan_size = 0.072
black_size = 0.09
dtr = 1.5

crx,cry = 0.25, 0.2

class PetangBall:
    def __init__(self, radius, position=None):
        self.radius = radius
        self.prev_position = position

        self.object_diameter = petan_radius  # Assume the diameter of the object in pixels
        self.object_real_size = petan_size  # The actual size of the object in meters
        self.pixel_to_meter = self.object_real_size / self.object_diameter
        self.speed = 0

        self.speed_pixels_x = 0
        self.speed_pixels_y = 0
            

        self.speed_meters_x = 0
        self.speed_meters_y = 0

        self.max_speed = 0
        self.speed_array = []
        self.time_array = []

    
    def move(self, current_time, elapsed_time, position):
        if self.prev_position is not None:
            ds = np.array(position) - np.array(self.prev_position)
            ds_meters = ds * self.pixel_to_meter
            dx, dy = ds
            dx_meters, dy_meters = ds_meters
                           
            distance = np.linalg.norm(ds)
            distance_meters = distance * self.pixel_to_meter

            self.speed = distance_meters / elapsed_time
            self.speed_array.append(self.speed)
            self.time_array.append(current_time)


            self.speed_pixels_x = dx / elapsed_time
            self.speed_pixels_y = dy / elapsed_time
            

            self.speed_meters_x = dx_meters / elapsed_time
            self.speed_meters_y = dy_meters / elapsed_time


            if self.speed > self.max_speed:
                self.max_speed = self.speed

        self.prev_position = position

    def includes(self, petan):
        x = petan.prev_position[0] - self.prev_position[0]
        y = petan.prev_position[1] - self.prev_position[1]
        radius = x ** 2 + y ** 2
        r2 = math.sqrt(radius)
        if r2 < self.radius *dtr:
            return True
        return False


    def label_text(self):
        return [f"Speed: {self.speed:.2f} m/s",f"Speed X:{self.speed_meters_x:.2f}",f"Speed Y: {self.speed_meters_y:.2f}"]


class PetangStorage:
    def __init__(self):
        self.objects = []
        self.last_petan = None
        self.last_frame = 0

    def update_contours(self,current_frame, contours):
        elapsed_time = (current_frame - self.last_frame)/1000

        for c in contours:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            petan = PetangBall(radius, (x, y))

            found = False
            for obj in self.objects:
                if obj.includes(petan):
                    found = True
                    # If the center lies in at least one known ball, then this is the same ball
                    obj.move(current_frame/1000, elapsed_time, petan.prev_position)
                    break

            if not found:
                self.objects.append(petan)

        for obj in self.objects:
            found = False
            if len(self.objects) <= 2:
                continue
            for c in contours:
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                petan = PetangBall(radius, (x, y))
                if petan.includes(obj):
                    found = True
                    break

            if not found:
                self.objects.remove(obj)

        self.last_frame = current_frame

    def draw_arrows(self, frame):

        for o in self.objects:
            x,y = int(o.prev_position[0]), int(o.prev_position[1])
    
            vx_position = (int(o.prev_position[0] + o.speed_pixels_x), int(o.prev_position[1]),)
            vy_position = (int(o.prev_position[0]), int(o.prev_position[1] + o.speed_pixels_y),)
            
            cv2.arrowedLine(frame, (x, y), vx_position, (0, 0, 255) , 5) 
            cv2.arrowedLine(frame, (x, y), vy_position, (255, 0, 0) , 5) 
    def draw_labels(self, frame):
        #if len(self.objects) > 2:  # For debugging
         #   print(f"{len(self.objects)} labels")

        for o in self.objects:
            x,y = int(o.prev_position[0]), int(o.prev_position[1])
            texts = o.label_text()
            for i in range(len(texts)):
                text = texts[i]
                cv2.putText(frame, text, (x + 100, y + i * 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

class SpeedMeasurementApp(QWidget):
    def __init__(self):
        super().__init__()
        self.speed_array = []
        self.time_array = []
        self.min_radius = 20
        self.max_radius = 100
        self.timer_ticks = 60
        self.setup_ui()
        self.setup_camera()

        self.storage = PetangStorage()


    def setup_ui(self):

        layout = QVBoxLayout()  # Move this line here

        self.speed_label = QLabel("Ball Speed Meter")
        self.image_label = QLabel()
        self.pause_button = QPushButton("Pause")
        #self.reset_button = QPushButton("Reset")
        self.resetspeed_button = QPushButton("Reset Speed")
        self.quit_button = QPushButton("Quit")

        self.quit_button.setStyleSheet("background-color: #BF5730")
        self.pause_button.setStyleSheet("background-color: #BF8130")
        self.resetspeed_button.setStyleSheet("background-color: #AA2A53")
        self.setStyleSheet("background-color: #218457")

        # Add sliders and labels to the layout
        layout.addWidget(self.speed_label)
        layout.addWidget(self.image_label)
        #layout.addWidget(self.reset_button)
        layout.addWidget(self.resetspeed_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.quit_button)

        self.pause_button.clicked.connect(self.pause_measurement)
        #self.reset_button.clicked.connect(self.reset_measurement)
        self.resetspeed_button.clicked.connect(self.resetspeed_measurement)
        self.quit_button.clicked.connect(self.close)

        self.setLayout(layout)
        self.setWindowTitle("Speed Measurement")
        self.show()

    def plot_speed_graph(self):
        plt.figure()
        for p in self.storage.objects:
            plt.plot(p.time_array, p.speed_array)
        plt.xlabel('Time')
        plt.ylabel('Speed')
        plt.title('Speed vs Time')
        plt.show()

    def setup_camera(self):
        self.cap = cv2.VideoCapture(0)  # Initialize cap with the default camera (you can change the camera index if needed)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(self.timer_ticks)

        self.prev_position = None
        self.speed = 0
        self.max_speed = 0
        self.real_time_speed = 0
        self.pause_measurement_flag = False


    def find_black_circles(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, threshold = cv2.threshold(blur, 60 , 255, cv2.THRESH_BINARY_INV)
        contours_, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours_

    def find_petan_circles(self, frame):
        sat = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)[:,:,1]
        blur = cv2.GaussianBlur(sat, (3, 3), 0)
        mask = 255 - cv2.threshold(blur, 100 , 255, cv2.THRESH_BINARY_INV)[1]
        kernel = np.ones((15,15), np.uint8) 
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        contours_, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return contours_
        
    def find_ball_circles(self, contours_, frame):
        
        contours = []

        for c in contours_:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            if radius > self.max_radius or radius < self.min_radius:
                continue

            center = (int(x),int(y))
            cv2.circle(frame,center,int(radius),(0,255,0),2)
            contours.append(c)

        return contours

    def crop_frame(self, frame, dx=0.1, dy=0.1):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        crop_height = int(height * dx)
        crop_width = int(width * dy)
        crop_height_to = height - crop_height
        crop_width_to = width-crop_width
        return frame[crop_height:crop_height_to, crop_width:crop_width_to]
        
    def update_frame(self):
        if not self.timer.isActive():
            return

        if self.pause_measurement_flag:
            return

        ret, frame = self.cap.read()
        if not ret:
            return
        current_frame = self.cap.get(cv2.CAP_PROP_POS_MSEC); # Get current frame number

        frame = self.crop_frame(frame, crx, cry)
        contours_ = self.find_black_circles(frame) + self.find_petan_circles(frame)
        contours = self.find_ball_circles(contours_, frame)
        
        self.storage.update_contours(current_frame, contours)

        # Converting an image from OpenCV to Qt
        self.storage.draw_arrows(frame)
        frame = cv2.resize(frame, (800, 800))
        self.storage.draw_labels(frame)
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)
        self.real_time_speed = self.speed
        self.last_frame  = current_frame

    def start_measurement(self):
        self.max_speed = 0
        self.time_start = time.time()

    """
    def reset_measurement(self):
        self.setup_camera()
        self.prev_position = None
        self.speed = 0
        self.max_speed = 0

        self.timer.start(self.timer_ticks)
        self.pause_measurement_flag = False
        self.pause_button.setText("Pause")

        self.time_array = []
        self.speed_array = []
    """

    def resetspeed_measurement(self):
        self.speed = 0
        self.max_speed = 0
        self.time_array = []
        self.speed_array = []

    def pause_measurement(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pause_measurement_flag = True
            self.pause_button.setText("Resume")
        else:
            self.timer.start(self.timer_ticks)
            self.pause_measurement_flag = False
            self.pause_button.setText("Pause")

    def closeEvent(self, event):
        self.cap.release()
        cv2.destroyAllWindows()
        self.plot_speed_graph() # Calling the matplotlib chart

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeedMeasurementApp()
    sys.exit(app.exec_())