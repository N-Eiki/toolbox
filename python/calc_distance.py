import argparse

import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("target_uuid", help="target uuid")
    parser.add_argument("rosbag_path", help="rosbag path")
    args = parser.parse_args()
    return args

def main(target_uuid, rosbag_path):
    
if __name__=="__main__":
    args = parse_args()
    main(args.target_uuid, args.rosbag_path)