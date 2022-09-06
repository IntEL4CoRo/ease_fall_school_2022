#!/bin/bash
source /home/workspace/ros/devel/setup.bash
roslaunch cram_pr2_pick_place_demo sandbox.launch --wait &
export THIS_IP=$(ifconfig 'docker0' | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*')
sleep 2
echo ""
echo ""
jupyter-lab --allow-root --no-browser --port 8888 --ip=0.0.0.0
