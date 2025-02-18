#!/bin/bash

# BAG_NAME=$1
# BAG_NAME=/home/eikinagata2/autoware_rosbag/xx1/jpt7/31c7ab0b-f3db-4c84-b930-8334fe5a48fe/1feddd62-ce45-41ee-bed6-3dcdb06ccc8e_2024-05-27-16-34-01_p0900_14.db3
BAG_NAME=/home/eikinagata2/autoware_rosbag/xx1/test/2c40269c-6ee8-49f6-ad94-ebba036f1e46/1feddd62-ce45-41ee-bed6-3dcdb06ccc8e_2024-08-19-15-06-27_p0900_17.db3 --start-offset 10
TARGET_TOPIC="
    /sensing/lidar/top/velodyne_packets \
    /sensing/lidar/left/velodyne_packets \
    /sensing/lidar/right/velodyne_packets \
    /sensing/lidar/rear/velodyne_packets \
    /sensing/lidar/left_upper/pandar_packets \
    /sensing/lidar/right_upper/pandar_packets \
    /vehicle/status/steering_status \
    /vehicle/status/velocity_status \
    /localization/kinematic_state \
    /tf \
    /sensing/camera/camera0/trigger_time\
    /sensing/camera/camera0/camera_info \
    /sensing/camera/camera0/image_rect_color/compressed \
    /sensing/camera/camera1/camera_info \
    /sensing/camera/camera1/image_rect_color/compressed \
    /sensing/camera/camera2/camera_info \
    /sensing/camera/camera2/image_rect_color/compressed \
    /sensing/camera/camera3/camera_info \
    /sensing/camera/camera3/image_rect_color/compressed \
    /sensing/camera/camera4/camera_info \
    /sensing/camera/camera4/image_rect_color/compressed \
    /sensing/camera/camera5/camera_info \
    /sensing/camera/camera5/image_rect_color/compressed \
    /sensing/camera/camera6/camera_info \
    /sensing/camera/camera6/image_raw/compressed\
    /sensing/radar/front_center/objects_raw \
    /sensing/radar/front_left/objects_raw \
    /sensing/radar/front_right/objects_raw \
    /sensing/radar/rear_center/objects_raw \
    /sensing/radar/rear_left/objects_raw \
    /sensing/radar/rear_right/objects_raw \
"

# TARGET_TOPIC="
#     /tf \
#     /tf_static \
#     /localization/kinematic_state \
#     /sensing/lidar/left/velodyne_packets \
#     /sensing/lidar/rear/velodyne_packets \
#     /sensing/lidar/right/velodyne_packets \
#     /sensing/lidar/top/velodyne_packets \
#     /vehicle/status/steering_status \
#     /vehicle/status/velocity_status \
#     /sensing/imu/tamagawa/imu_raw \
#     /sensing/gnss/septentrio/nav_sat_fix \
#     /sensing/gnss/ublox/nav_sat_fix \
#     /sensing/gnss/pose_with_covariance \
#     /sensing/camera/camera0/trigger_time
#     /sensing/camera/camera0/camera_info \
#     /sensing/camera/camera0/image_rect_color/compressed \
#     /sensing/camera/camera1/camera_info \
#     /sensing/camera/camera1/image_rect_color/compressed \
#     /sensing/camera/camera2/camera_info \
#     /sensing/camera/camera2/image_rect_color/compressed \
#     /sensing/camera/camera3/camera_info \
#     /sensing/camera/camera3/image_rect_color/compressed \
#     /sensing/camera/camera4/camera_info \
#     /sensing/camera/camera4/image_rect_color/compressed \
#     /sensing/camera/camera5/camera_info \
#     /sensing/camera/camera5/image_rect_color/compressed \
#     /sensing/camera/camera6/camera_info \
#     /sensing/camera/camera6/image_raw/compressed\
#     /sensing/radar/front_center/objects_raw \
#     /sensing/radar/front_left/objects_raw \
#     /sensing/radar/front_right/objects_raw \
#     /sensing/radar/rear_center/objects_raw \
#     /sensing/radar/rear_left/objects_raw \
#     /sensing/radar/rear_right/objects_raw \
#     /perception/traffic_light_recognition/traffic_signals"



ros2 bag play $BAG_NAME --topics $TARGET_TOPIC --clock 10 -r 1.0