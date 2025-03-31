
"""
使い方
git clone https://github.com/N-Eiki/toolbox
source ~/autoware.proj/install/setup.bash
cd ~/toolbox/python

uuidがb8e0のものに対してx, yの距離を描画する
ただし、baselinkが一定である(egoが移動しない)ことが条件
python3 show_nvtl.py --rosbag_path=/apth/to/data/79c2eed3-dddd-40e5-b54c-0b3ce38b90fc_2025-02-13-13-57-48_p0900_2.db3


"""
import os

import argparse
import numpy as np

import matplotlib.pyplot as plt

from parse_function import parse_rosbag

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--rosbag_path", help="rosbag path")
    args = parser.parse_args()
    return args

def parse_baselink(msg):
    if msg.transforms[0].child_frame_id!="base_link":
        return None
    # return msg
    return [msg.transforms[0].transform.translation.x, msg.transforms[0].transform.translation.y, msg.transforms[0].transform.translation.z]


def parse_nvtl(msg):
    return [msg.data]


def extract_data(rosbag_path:str):
    nvtl_topic = "/localization/pose_estimator/nearest_voxel_transformation_likelihood"
    nvtl_dict = parse_rosbag(str(rosbag_path), [nvtl_topic], parse_nvtl)
    return nvtl_dict[nvtl_topic].values



def main(rosbag_path: str):
    print(rosbag_path)
    # rosbag_pathが存在するか
    if not os.path.exists(rosbag_path):
        raise ValueError(f"{rosbag_path} is not exists")
    # rosbag_pathがfileか
    elif rosbag_path.endswith(".db3"):
        nvtl = extract_data(rosbag_path)
    # show image
    plt.plot(nvtl, label="nvtl data")

    # 最小値・最大値の線を引く
    min_val = np.min(nvtl)
    max_val = np.max(nvtl)
    plt.axhline(y=min_val, color='blue', linestyle='dashed', label=f'Min: {min_val:.2f}')
    plt.axhline(y=max_val, color='red', linestyle='dashed', label=f'Max: {max_val:.2f}')

    plt.legend()
    plt.show()

if __name__=="__main__":
    args = parse_args()
    main(args.rosbag_path)