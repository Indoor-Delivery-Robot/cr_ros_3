#!/usr/bin/env python

# Description: publishes current state of the robot, enumerates possible state_sub
# and legal state changes

# changes in cr_ros_2: removed the states docked and docking which were unique to
# the physical structure of the turtlebot 2
# --> added namespacing to the service name and subscribed topic

from enum import Enum
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose, Point
from cr_ros_2.srv import *

__change_state = rospy.ServiceProxy('state_change', StateChange)


class States(Enum):

    WAITING = 'WAITING'
    NAVIGATING = 'NAVIGATING'
    TELEOP = 'TELEOP'
    LOST = 'LOST'
    FLYING = 'FLYING'
    STOLEN_PACKAGE = 'STOLEN_PACKAGE'
    SEARCH = 'SEARCH'


    ILLEGAL_STATE_CHANGE = 'ILLEGAL_STATE_CHANGE'

    DUMMY_POSE = Pose(position=Point(z=1))
    DUMMY_STRING = 'n0th1ng_t0_s4y'


def change_state(new_state,
                to_say=States.DUMMY_STRING.value,
                pose_to_pub=States.DUMMY_POSE.value):
    req = StateChangeRequest(new_state.value, to_say, pose_to_pub)
    return __change_state(req)

legal_state_changes = {
        States.WAITING: [
            States.NAVIGATING,
            States.TELEOP,
            States.FLYING,
            States.STOLEN_PACKAGE,
            States.SEARCH,
        ],
        States.NAVIGATING: [
            States.TELEOP,
            States.FLYING,
            States.WAITING,
            States.STOLEN_PACKAGE,
            States.SEARCH,
        ],
        States.TELEOP: [
            States.WAITING,
            States.FLYING,
            States.LOST,
        ],
        States.ILLEGAL_STATE_CHANGE: [
            States.FLYING,
            States.LOST,
            States.WAITING,
            States.TELEOP,
        ],
        States.LOST: [
            States.WAITING,
            States.FLYING,
            States.TELEOP,
        ],
        States.FLYING: [
            States.LOST,
        ],
        States.SEARCH: [
            States.NAVIGATING,
            States.WAITING,
        ],
        States.STOLEN_PACKAGE: [
            States.NAVIGATING,
            States.WAITING,
        ],
        # States.LOCALIZING: [States.NAVIGATING, States.WAITING],
        # States.CLEARING_COSTMAP: [States.NAVIGATING, States.TELEOP],
        # States.DONE_NAVIGATING: [States.WAITING],
    }

def state_cb(msg):
    global current_state
    current_state = States[msg.data]

def get_state():
    return current_state

state_sub = rospy.Subscriber('state', String, state_cb)
