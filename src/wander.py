#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

def scan_callback(msg):
	#define the variable for controlling distance to objects
	global g_range_ahead

	# Read the laser sensor data for the 40 degrees range in front of the robot
	g_range_ahead = min(msg.ranges[0:20] + msg.ranges[340:360])

g_range_ahead = 1 #anything to start

#scan with the laser scanner
scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback)

#tell the robot to move according to the laser data
cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)

#initiate the robot communication node
rospy.init_node('wander')

#take current time
state_change_time = rospy.Time.now()

#tell robot to move forward = true
driving_forward = True

#send 10 orders per second at maximum
rate = rospy.Rate(10)

#if robot is not turned off
while not rospy.is_shutdown():

	#if robot is moving forward
	if driving_forward:

		#stop the robot if the distance is less than 60 centimeters in front of the robot
		if (g_range_ahead < 0.6 or rospy.Time.now() > state_change_time):
			print("Rotating...")
			driving_forward = False
			state_change_time = rospy.Time.now() + rospy.Duration(0.1)
	else:
		if rospy.Time.now() > state_change_time:
			print("Moving...")
			driving_forward = True

			#move for 30 seconds at maximum, then stop
			state_change_time = rospy.Time.now() + rospy.Duration(30)
	twist = Twist()
	if driving_forward:
		#move the robot forward if it there are no obstacles
		twist.linear.x = 0.5
	else:
		#rotate the robot if it is not moving
		twist.angular.z = 1
	cmd_vel_pub.publish(twist)

	#wait between the orders
	rate.sleep()