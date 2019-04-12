#!/usr/bin/env bash

# This script executes the 'ds4drv' program to enable connection
# of a Dualshock 4 controller
#
# Used in ROS launch file for convenient launching.
# uinput permissions must be set to avoid running as root,
# see: https://github.com/chrippa/ds4drv#permissions

ds4drv