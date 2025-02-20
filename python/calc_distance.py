
"""
使い方
git clone https://github.com/N-Eiki/toolbox
cd ~/toolbox/python

uuidがb8e0のものに対してx, yの距離を描画する
ただし、baselinkが一定である(egoが移動しない)ことが条件
python3 calc_distance.py --target_uuid=b8e0\
                         --rosbag_path=/apth/to/data/79c2eed3-dddd-40e5-b54c-0b3ce38b90fc_2025-02-13-13-57-48_p0900_2.db3


自車両が移動したりして対象物体のuuidが変わってしまった場合lsim上のuuidを片っ端から乗せる
pathにrosbag単体のdb3だけではなく、db3の入ったディレクトリも指定できるように

python3 calc_distance.py --target_uuid b8e0 dc8d 975a ad13 05b8 1108 df2a \
                         --rosbag_path ../data/

"""
import os

import argparse
import numpy as np

import matplotlib.pyplot as plt
from natsort import natsorted

from parse_function import parse_rosbag

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_uuid', required=True, nargs="*", type=str, help='target uuid list')

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


def extract_data(rosbag_path:str, target_uuid: list[str]):
    perception_topic = "/perception/object_recognition/objects"
    baselink_topic = "/tf"
    perception_dict = parse_rosbag(str(rosbag_path), [perception_topic], parse_predicted_objects)
    baselink_dict = parse_rosbag(str(rosbag_path), [baselink_topic], parse_baselink)
    label = None
    pos_x, pos_y, vel_x, vel_y = [], [], [], []
    for record in perception_dict[perception_topic].values:
        for obj in record[0]:
            label = obj[1]
            if obj[0] not in target_uuid:
                continue
            pos_x.append(obj[2])
            pos_y.append(obj[3])
            vel_x.append(obj[4])
            vel_y.append(obj[5])
            break
    baselink_x, baselink_y, baselink_z = baselink_dict[baselink_topic].mean(axis=0)

    distance_x = np.array(pos_x) - baselink_x
    distance_y = np.array(pos_y) - baselink_y

    return distance_x, distance_y, vel_x, vel_y



def main(target_uuid: list[str], rosbag_path: str):
    print(rosbag_path)
    distance_x, distance_y, vel_x, vel_y = [], [], [], []
    # rosbag_pathが存在するか
    if not os.path.exists(rosbag_path):
        raise ValueError(f"{rosbag_path} is not exists")
    # rosbag_pathがfileか
    elif rosbag_path.endswith(".db3"):
        distance_x, distance_y, vel_x, vel_y = extract_data(rosbag_path, target_uuid)
    # rosbag_pathがdirか？
    else:
        data = [f for f in os.listdir(rosbag_path) if f.endswith("db3")]
        for file in data:
            file_path = os.path.join(rosbag_path, file)
            _distance_x, _distance_y, _vel_x, _vel_y = extract_data(file_path, target_uuid)
            distance_x = np.append(distance_x, _distance_x)
            distance_y = np.append(distance_y, _distance_y)
            vel_x = np.append(vel_x, _vel_x)
            vel_y = np.append(vel_y, _vel_y)
            

    fig, ax = plt.subplots(2, 1, figsize=(8, 5))
    fig.suptitle('title')
    # 最初のサブプロット
    ax[0].plot(distance_x, label="x distance [m]")
    ax[0].plot(distance_y, label="y distance [m]")
    ax[0].set_title("Position Difference")
    ax[0].legend()  # 凡例を表示

    # 2番目のサブプロット
    ax[1].plot(vel_x, label="x velocity [m/s]")
    ax[1].plot(vel_y, label="y velocity [m/s]")
    ax[1].set_title("Target Velocicty")
    ax[1].legend()  # 凡例を表示

    plt.show()

    import ipdb;ipdb.set_trace()

if __name__=="__main__":
    args = parse_args()
    main(args.target_uuid, args.rosbag_path)