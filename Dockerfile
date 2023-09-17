FROM ros:humble

# Install curl, vim, tmux

RUN apt-get update
RUN apt-get install -y curl vim tmux ros-humble-rosbridge-server
RUN apt-get install -y python3-pip build-essential libcap-dev
RUN apt-get update && apt-get install -y ros-humble-cv-bridge
RUN pip3 install rpi.gpio
RUN pip3 install smbus

# Create workspace

RUN mkdir -p ~/ros2_ws/src

COPY ./Car.py /root/
COPY ./Ultrasonic.py /root/