# vision-object-tracking-esp32
ESP32-based vision object tracking system using Python, OpenCV, servo control, ultrasonic distance measurement, and a web dashboard.
# Vision-Based Object Tracking & Distance Monitoring System

## Overview

This project uses a laptop camera with Python and OpenCV to detect an
object and determine whether it is positioned on the left, center,
or right side of the camera frame.

The detected position is sent wirelessly to an ESP32, which controls
a servo motor. An HC-SR04 ultrasonic sensor measures distance, while
an ESP32 web dashboard provides real-time monitoring.

## Features

- Object detection using OpenCV
- LEFT / CENTER / RIGHT position detection
- Wireless Python-to-ESP32 communication
- Automatic servo positioning
- Ultrasonic distance measurement
- ESP32 web dashboard
- Real-time system monitoring

## Hardware

- ESP32
- HC-SR04 ultrasonic sensor
- SG90 servo motor
- Laptop camera
- External 5V supply for servo

## Software

- Arduino IDE
- Python
- OpenCV
- Requests
