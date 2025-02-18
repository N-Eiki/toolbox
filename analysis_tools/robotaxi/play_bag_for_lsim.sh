#!/bin/bash

BAG_NAME=$1
TARGET_TOPIC="
    /tf \
    /tf_static \
    /localization/kinematic_state \
    /sensing/lidar/rear_upper/pandar_packets \
    /sensing/lidar/front_lower/pandar_packets \
    /sensing/lidar/rear_lower/pandar_packets \
    /sensing/lidar/front_upper/pandar_packets \
    /sensing/lidar/left_upper/pandar_packets \
    /sensing/lidar/right_upper/pandar_packets \
    /sensing/lidar/left_lower/pandar_packets \
    /sensing/lidar/right_lower/pandar_packets \
    /vehicle/status/steering_status \
    /vehicle/status/velocity_status \
    /sensing/imu/tamagawa/imu_raw \
    /sensing/gnss/septentrio/nav_sat_fix \
    /sensing/gnss/ublox/nav_sat_fix \
    /sensing/gnss/pose_with_covariance \
    /sensing/camera/camera0/trigger_time
    /sensing/camera/camera0/camera_info \
    /sensing/camera/camera0/image_rect_color/compressed \
    /sensing/camera/camera1/camera_info \
    /sensing/camera/camera1/image_rect_color/compressed \
    /sensing/camera/camera1/trigger_time \
    /sensing/camera/camera2/camera_info \
    /sensing/camera/camera2/image_rect_color/compressed \
    /sensing/camera/camera2/trigger_time \
    /sensing/camera/camera3/camera_info \
    /sensing/camera/camera3/image_rect_color/compressed \
    /sensing/camera/camera3/trigger_time \
    /sensing/camera/camera4/trigger_time \
    /sensing/camera/camera5/camera_info \
    /sensing/camera/camera5/image_rect_color/compressed \
    /sensing/camera/camera5/trigger_time \
    /sensing/camera/camera6/camera_info \
    /sensing/camera/camera6/image_rect_color/compressed \
    /sensing/camera/camera6/trigger_time \
    /sensing/camera/camera7/camera_info \
    /sensing/camera/camera7/image_raw/compressed \
    /sensing/camera/camera7/trigger_time \
    /sensing/radar/front_center/objects_raw \
    /sensing/radar/front_left/objects_raw \
    /sensing/radar/front_right/objects_raw \
    /sensing/radar/rear_center/objects_raw \
    /sensing/radar/rear_left/objects_raw \
    /sensing/radar/rear_right/objects_raw \"
    # /perception/traffic_light_recognition/traffic_signals "

ros2 bag play $BAG_NAME --topics $TARGET_TOPIC --clock 10 -r 1.0
