#!/usr/bin/env python

# M. Kaan Tasbas | mktasbas@gmail.com
# Eyes of Argus
# February 2019

# This script publishes linear and angular velocities that
# without setting the other to zero like the original joyop.
# This allows more continous, curve like motion rather than
# the blocky movement of the original.

import rospy
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist


def callback(data):
    vel_publisher = rospy.Publisher('/joyop/cmd_vel', Twist, queue_size=5)
    cmd = Twist()

    deadzone = 0.10  # percentage, increased deadzone decreases joystick sensitivity
    max_linear_vel = 4.0
    max_angular_vel = 4.0

    #rospy.loginfo("Joyop: max_linear_vel = %f, max_angular_vel = %f", max_linear_vel, max_angular_vel)

    cmd.linear.x = 0
    cmd.linear.y = 0
    cmd.linear.z = 0
    cmd.angular.x = 0
    cmd.angular.y = 0
    cmd.angular.z = 0

    #rospy.loginfo(rospy.get_caller_id() + "Left: %f, Right: %f",
    #              data.axes[1], data.axes[5])
    
    left_joy = data.axes[1]
    right_joy = data.axes[5]
    left_plus_right = (left_joy + right_joy) / 2
    left_minus_right = (left_joy - right_joy) / 2

    # Linear: Add joystick values, divide by 2
        # if > deadzone, move forward (+)
        # if < deadzone, move backwards (-)
    # Angular: Subtract left - right, divide by 2
        # if > deadzone, turn clockwise (+)
        # if < deadzone, turn counterclockwise (-)

    # linear
    if left_plus_right > -deadzone and left_plus_right < deadzone:
        # in deadzone, no linear velocity
        cmd.linear.x = 0
    elif left_plus_right > deadzone:
        # above deadzone, move forward
        cmd.linear.x = left_plus_right * max_linear_vel
    elif left_plus_right < deadzone:
        # below deadzone, move backwards
        cmd.linear.x = left_plus_right * max_linear_vel

    # angular
    if left_minus_right > -deadzone and left_minus_right < deadzone:
        # in deadzone, no angular velocity
        cmd.angular.z = 0
    elif left_minus_right > deadzone:
        # left > right, above deadzone, turn clockwise
        cmd.angular.z = -(left_minus_right * max_angular_vel)
    elif left_minus_right < deadzone:
        # left < right, below deadzone, turn counterclockwise
        cmd.angular.z = -(left_minus_right * max_angular_vel)

    vel_publisher.publish(cmd)

def joyop():
    rospy.init_node('joyop')
    rospy.Subscriber("joy", Joy, callback)
    
    rospy.spin()


if __name__ == '__main__':
    try:
        joyop()
    except rospy.ROSInterruptException:
        pass
