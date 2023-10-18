import cv2
import numpy as np
import PySimpleGUI as sg
import os

# Initialize the video capture from the default camera (index 0)
video = cv2.VideoCapture(0)

# Initialize the scaling factor for zooming
scale = 100

# Define a function called "funct" that takes a video source as an argument
def funct(video):
    global scale  # Make 'scale' a global variable so we can modify it in this function
    while True:
        # Read a frame from the video source
        (grabbed, frame) = video.read()
        if not grabbed:
            break

        # Resize the frame to a fixed size (480x270)
        frame = cv2.resize(frame, (480, 270))

        # Apply Gaussian blur to the frame
        blur = cv2.GaussianBlur(frame, (21, 21), 0)
        hsv = blur

        # Define color ranges for red and white in HSV format
        lowerred = [60, 60, 120]
        upperred = [160, 200, 255]
        lowerred = np.array(lowerred, dtype="uint8")
        upperred = np.array(upperred, dtype="uint8")

        lowerwhite = [200, 200, 200]
        upperwhite = [255, 255, 255]
        lowerwhite = np.array(lowerwhite, dtype="uint8")
        upperwhite = np.array(upperwhite, dtype="uint8")

        # Create masks for red and white colors
        maskred = cv2.inRange(hsv, lowerred, upperred)
        maskwhite = cv2.inRange(hsv, lowerwhite, upperwhite)

        # Apply masks to the frame to isolate red and white colors
        outputred = cv2.bitwise_and(frame, hsv, mask=maskred)
        outputwhite = cv2.bitwise_and(frame, hsv, mask=maskwhite)

        # Combine the red and white masked images
        redwhite = outputred + outputwhite

        # Convert the combined image to grayscale
        gray = cv2.cvtColor(redwhite, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to the grayscale image
        (thresh1, gray) = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY_INV)

        # Detect circles in the grayscale image using Hough Circle Transform
        detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=1, maxRadius=40)
        fires_detected = 0

        # Create a mask to isolate detected circles
        mask = np.zeros_like(gray)
        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))
            for pt in detected_circles[0, :]:
                (x, y, r) = pt

                # Draw circles and calculate average color in the circle
                cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
                cv2.circle(frame, (x, y), 1, (0, 0, 255), 3)
                cv2.circle(mask, (x, y), r, 255, -1)
                avg_color = cv2.mean(frame, mask=mask)[:3]

                # Check if the average color falls within a certain range (fire color)
                if avg_color[0] >= 115 and avg_color[0] <= 175 and avg_color[1] >= 195 and avg_color[1] <= 255 and avg_color[2] >= 155 and avg_color[2] <= 230:
                    fires_detected += 1
                    print(avg_color)

                    # Highlight the circle in purple
                    cv2.circle(frame, (x, y), r, (255, 0, 255), 2)
                    cv2.circle(frame, (x, y), 1, (255, 0, 255), 3)

        else:
            fires_detected = 0

        # Display the number of detected fires on the frame
        if fires_detected >= 1:
            frame = cv2.putText(frame, str(fires_detected) + ' fires', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 1, cv2.LINE_AA)

        # Flip the frame horizontally
        image = frame
        image = cv2.flip(image, 1)

        # Calculate the cropping area based on the scaling factor
        height, width, channels = image.shape
        centerX, centerY = int(height/2), int(width/2)
        radiusX, radiusY = int(scale*height/100), int(scale*width/100)
        minX, maxX = centerX - radiusX, centerX + radiusX
        minY, maxY = centerY - radiusY, centerY + radiusY

        # Crop and resize the frame
        cropped = image[minX:maxX, minY:maxY]
        resized_cropped = cv2.resize(cropped, (width, height))

        # Check for key presses to adjust the scaling factor
        key = cv2.waitKey(10)
        if key & 0xFF == ord('1') and scale < 200:
            scale += 10  # Zoom in
            print("Zoom In")
        elif key & 0xFF == ord('2') and scale > 10:
            scale -= 10  # Zoom out
            print("Zoom Out")

        # Display the zoomed frame
        cv2.imshow('Zoomed Frame', resized_cropped)

# Define the GUI layout using PySimpleGUI with improved aesthetics
sg.theme('DarkTeal5')  # Set the theme to Dark Teal
layout = [
    [sg.Text('Fire Detection System', font=('Any 18')), sg.Image(filename='fire.png')],
    [sg.Button('Start', size=(8, 2), key='Start', font=('Any 14')), sg.Exit(font=('Any 14'),size=(8,2))],
]

# Create a PySimpleGUI window
window = sg.Window('Fire Detection System', layout, resizable=True)

while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    elif event == 'Start':
        funct(video)

# Release the OpenCV resources and close the GUI window
cv2.destroyAllWindows()
video.release()
