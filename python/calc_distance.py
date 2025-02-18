
"""
使い方
git clone https://github.com/N-Eiki/toolbox
cd ~/toolbox/python

uuidがb8e0のものに対してx, yの距離を描画する
ただし、baselinkが一定である(egoが移動しない)ことが条件
python3 calc_distance.py --target_uuid=b8e0\
                         --rosbag_path=/apth/to/data/79c2eed3-dddd-40e5-b54c-0b3ce38b90fc_2025-02-13-13-57-48_p0900_2.db3
"""
import argparse
import numpy as np

import matplotlib.pyplot as plt

from parse_function import parse_rosbag

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_uuid", help="target uuid")
    parser.add_argument("--rosbag_path", help="rosbag path")
    args = parser.parse_args()
    return args

def parse_baselink(msg):
    if msg.transforms[0].child_frame_id!="base_link":
        return None
    # return msg
    return [msg.transforms[0].transform.translation.x, msg.transforms[0].transform.translation.y, msg.transforms[0].transform.translation.z]


def parse_predicted_objects(msg):
    obj_data = []
    for obj in msg.objects:
        uuid = obj.object_id.uuid
        # [TODO]複数ラベルのときの挙動を修正、一番probabilityが高いのがindex=0ならこのままでよいか
        label = obj.classification[0].label
        #xyz position
        pos_x = obj.kinematics.initial_pose_with_covariance.pose.position.x
        pos_y = obj.kinematics.initial_pose_with_covariance.pose.position.y
        pos_z = obj.kinematics.initial_pose_with_covariance.pose.position.z

        vel_x = obj.kinematics.initial_twist_with_covariance.twist.linear.x
        vel_y = obj.kinematics.initial_twist_with_covariance.twist.linear.y

        ang_x = obj.kinematics.initial_twist_with_covariance.twist.angular.x
        ang_y = obj.kinematics.initial_twist_with_covariance.twist.angular.y
        ang_z = obj.kinematics.initial_twist_with_covariance.twist.angular.z

        # acc.x = obj.kinematics.initial_acceleration_with_covariance.accel.x
        # acc.y = obj.kinematics.initial_acceleration_with_covariance.accel.y
        # acc.z = obj.kinematics.initial_acceleration_with_covariance.accel.z
        obj_data.append([
            hex(uuid[0])[-2:]+hex(uuid[1])[-2:],
            label,
            pos_x,
            pos_y,
            vel_x,
            vel_y,
        ])
    return [obj_data]

def main(target_uuid, rosbag_path):
    perception_topic = "/perception/object_recognition/objects"
    baselink_topic = "/tf"
    print(rosbag_path)
    perception_dict = parse_rosbag(str(rosbag_path), [perception_topic], parse_predicted_objects)
    baselink_dict = parse_rosbag(str(rosbag_path), [baselink_topic], parse_baselink)
    label = None
    pos_x, pos_y, vel_x, vel_y = [], [], [], []
    for record in perception_dict[perception_topic].values:
        for obj in record[0]:
            label = obj[1]
            if obj[0] != target_uuid:
                continue
            pos_x.append(obj[2])
            pos_y.append(obj[3])
            vel_x.append(obj[4])
            vel_y.append(obj[5])
            break
    baselink_x, baselink_y, baselink_z = baselink_dict[baselink_topic].mean(axis=0)
    plt.plot(np.array(pos_x)-baselink_x, label="x distance[m]")
    plt.plot(np.array(pos_y)-baselink_y, label="y distance[m]")
    plt.legend()
    plt.show()

    import ipdb;ipdb.set_trace()

if __name__=="__main__":
    args = parse_args()
    main(args.target_uuid, args.rosbag_path)