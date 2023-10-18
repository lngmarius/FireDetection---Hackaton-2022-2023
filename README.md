# FireDetection---Hackaton-2022-2023
Fire Detection system - Hackathon 2022/2023

This Python project is a fire detection system that uses computer vision techniques to detect fires in real-time video streams. The program leverages the OpenCV library for video capture and image processing and PySimpleGUI for a basic graphical user interface (GUI). It allows users to adjust the zoom level and start the fire detection process.

This project was developed as part of the Hackhaton 2022/2023 competition.

**Getting Started**

To get started with this fire detection system, you will need to have Python and a few libraries installed. You can follow these steps to set up the project:

1. Clone the Repository 

Clone this repository to your local machine using Git:

    git clone https://github.com/your-username/fire-detection-system.git

2. Install Dependencies

Navigate to the project directory and install the required Python dependencies using pip:

    pip install opencv-python numpy PySimpleGUI

3. Run the Program

Execute the main Python script to start the fire detection system:

    python fire_detection.py

**Features**

Real-time fire detection using computer vision techniques.
Adjustable zoom level for focusing on specific areas.
Graphical user interface for user interaction.
Detection of fires based on color and shape analysis.

**Usage**

1.Upon running the program, you will be presented with a GUI window with a "Start" button.

2.Click the "Start" button to initiate the fire detection process. The system will capture video from the default camera (usually the built-in webcam) and start analyzing it for fires.

3.Adjust the zoom level using the following key commands:

        Press '1' to zoom in (increases zoom scale).
        Press '2' to zoom out (decreases zoom scale).
        
4.The system will detect and highlight fires in the video stream in purple color. The number of detected fires is displayed in the top-left corner.

5.To exit the program, close the GUI window or press the "Exit" button.

