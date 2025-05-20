#!/usr/bin/env python3

import os
import glob
import yaml
from typing import Dict, Tuple, List, Optional


def load_sensor_kit_calibration(base_path: str) -> Dict[str, Dict]:
    """センサーキットのキャリブレーション情報を読み込む"""
    calibration_file = os.path.join(base_path, "sensor_kit_calibration.yaml")
    try:
        with open(calibration_file, 'r') as f:
            config = yaml.safe_load(f)
        return config.get('sensor_kit_base_link', {})
    except Exception as e:
        print(f"[ERROR] Failed to load calibration file: {e}")
        return {}


def extract_camera_info(param_file: str, calibration_data: Dict[str, Dict], is_v4l2: bool) -> Optional[Tuple[str, str, Dict, str]]:
    """パラメータファイルからカメラ情報を抽出"""
    try:
        with open(param_file, 'r') as f:
            config = yaml.safe_load(f)

        if is_v4l2:
            frame_id = config['/**']['ros__parameters']['camera_frame_id']
            camera_num = os.path.basename(param_file).split('_')[1].split('.')[0]
        else:
            ros_params = config['/**']['ros__parameters']
            camera_name = ros_params['camera_name']
            frame_id = ros_params['frame_id']
            camera_num = camera_name.replace('camera', '')

        location = frame_id.replace('/camera_optical_link', '')
        coords = calibration_data.get(f"{location}/camera_link", {})
        topic = f'/sensing/camera/camera{camera_num}/image_raw/compressed'

        return camera_num, location, coords, topic
    except Exception as e:
        print(f"[ERROR] Failed to process {param_file}: {e}")
        return None


def find_camera_mappings(base_path: str) -> Dict[str, Tuple[str, Dict, str]]:
    """カメラ番号と設置場所のマッピングを取得"""
    camera_files = glob.glob(os.path.join(base_path, "tier4-c2", "camera*_sxpf.param.yaml"))
    v4l2_files = glob.glob(os.path.join(base_path, "tier4-c2", "v4l2_*.param.yaml"))

    calibration_data = load_sensor_kit_calibration(base_path)
    camera_mappings = {}

    for param_file in camera_files:
        result = extract_camera_info(param_file, calibration_data, is_v4l2=False)
        if result:
            camera_num, location, coords, topic = result
            camera_mappings[camera_num] = (location, coords, topic)

    for param_file in v4l2_files:
        result = extract_camera_info(param_file, calibration_data, is_v4l2=True)
        if result:
            camera_num, location, coords, topic = result
            camera_mappings[camera_num] = (location, coords, topic)

    return camera_mappings


def project_coordinates(coords_list: List[float], out_min: int, out_max: int, reverse: bool = False) -> List[int]:
    """リストの値を指定範囲に正規化して整数に変換"""
    min_val = min(coords_list)
    max_val = max(coords_list)
    scale = (out_max - out_min) / (max_val - min_val) if max_val != min_val else 1
    projected = [int((val - min_val) * scale + out_min) for val in coords_list]
    return [out_max - val if reverse else val for val in projected]


def get_camera_positions(base_path: str) -> Dict[int, Tuple[int, int]]:
    """カメラの表示位置 (f, s) を計算して返す"""
    if not os.path.exists(base_path):
        print(f"[ERROR] Path not found: {base_path}")
        return {}

    mappings = find_camera_mappings(base_path)
    coords_data = []

    for cam_num in sorted(mappings.keys(), key=int):
        _, coords, _ = mappings[cam_num]
        if 'y' in coords and 'x' in coords:
            f = coords['y']
            s = coords['x']
            coords_data.append((int(cam_num), f, s))

    # ソート: fが小さい → sが小さい順
    coords_data.sort(key=lambda item: (item[1], item[2]))

    front_coords = [f for _, f, _ in coords_data]
    side_coords = [s for _, _, s in coords_data]

    front_proj = project_coordinates(front_coords, 110, 610)
    side_proj = project_coordinates(side_coords, 200, 700, reverse=True)

    camera_positions = {}
    for i, (cam_num, f, s) in enumerate(coords_data):
        f_pos = front_proj[i]
        s_pos = side_proj[i]
        print(f"camera{cam_num}: ({f_pos}, {s_pos})")
        camera_positions[cam_num] = (f_pos, s_pos)

    return camera_positions


def print_camera_mappings(mappings: Dict[str, Tuple[str, Dict, str]]):
    """マッピング情報を表形式で出力"""
    print("\nカメラ番号と設置場所の紐付け:")
    print("-" * 120)
    print("カメラ番号\t設置場所\t\t座標 (x, y, z)\t\t\tトピック名")
    print("-" * 120)
    for camera_num in sorted(mappings.keys(), key=int):
        location, coords, topic = mappings[camera_num]
        x = coords.get('x', 'N/A')
        y = coords.get('y', 'N/A')
        z = coords.get('z', 'N/A')
        print(f"{camera_num}\t\t{location}\t({x}, {y}, {z})\t{topic}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="カメラ番号と表示位置の取得")
    parser.add_argument('--base_path', required=True, help='設定ファイルのベースパス')
    args = parser.parse_args()

    # マッピング情報取得・表示
    mappings = find_camera_mappings(args.base_path)
    print_camera_mappings(mappings)

    # 表示位置計算
    get_camera_positions(args.base_path)


if __name__ == "__main__":
    main()
