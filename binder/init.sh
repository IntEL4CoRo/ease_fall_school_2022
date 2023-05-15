#!/bin/bash

source ${HOME}/workspace/ros/devel/setup.bash

roscore &
roslaunch --wait cram_projection_demos household_pr2.launch &
roslaunch --wait rvizweb rvizweb.launch config_name:=cram_projection_demos &
roslaunch --wait ${PWD}/binder/reset_pr2.launch msg_file:=${PWD}/binder/reset_pr2.txt &

xvfb-run exec "$@"
