#!/usr/bin/env python3

import os
import yaml
import glob
from typing import Dict, List, Tuple

def load_sensor_kit_calibration(base_path: str) -> Dict[str, Dict]:
    """
    センサーキットのキャリブレーション情報を読み込む
    Args:
        base_path: 設定ファイルのベースパス
    Returns:
        センサー位置情報の辞書
    """
    calibration_file = os.path.join(base_path, "sensor_kit_calibration.yaml")
    try:
        with open(calibration_file, 'r') as f:
            config = yaml.safe_load(f)
        return config.get('sensor_kit_base_link', {})
    except Exception as e:
        print(f"Error loading calibration file: {e}")
        return {}

def find_camera_mappings(base_path: str) -> Dict[str, Tuple[str, Dict, str]]:
    """
    カメラ番号と設置場所の紐付けを取得する
    Args:
        base_path: 設定ファイルのベースパス
    Returns:
        カメラ番号と設置場所、座標、トピック名の紐付け辞書
    """
    # カメラ設定ファイルのパスを取得
    camera_param_files = glob.glob(os.path.join(base_path, "tier4-c2", "camera*_sxpf.param.yaml"))
    v4l2_param_files = glob.glob(os.path.join(base_path, "tier4-c2", "v4l2_*.param.yaml"))
    
    # センサーキットのキャリブレーション情報を読み込む
    calibration_data = load_sensor_kit_calibration(base_path)
    
    # カメラ番号と設置場所の紐付けを格納する辞書
    camera_mappings = {}
    
    # camera*_sxpf.param.yamlファイルの処理
    for param_file in camera_param_files:
        try:
            with open(param_file, 'r') as f:
                config = yaml.safe_load(f)
            # カメラ名とフレームIDを取得
            camera_name = config['/**']['ros__parameters']['camera_name']
            frame_id = config['/**']['ros__parameters']['frame_id']
            # カメラ番号を取得（camera<N>から<N>を抽出）
            camera_num = camera_name.replace('camera', '')
            # 設置場所を取得（frame_idからcamera_optical_linkを除去）
            location = frame_id.replace('/camera_optical_link', '')
            # 座標情報を取得
            coords = calibration_data.get(f"{location}/camera_link", {})
            # トピック名を生成
            topic = f'/sensing/camera/camera{camera_num}/image_raw/compressed'
            camera_mappings[camera_num] = (location, coords, topic)
        except Exception as e:
            print(f"Error processing {param_file}: {e}")
    
    # v4l2_*.param.yamlファイルの処理
    for param_file in v4l2_param_files:
        try:
            with open(param_file, 'r') as f:
                config = yaml.safe_load(f)
            # フレームIDを取得
            frame_id = config['/**']['ros__parameters']['camera_frame_id']
            # ファイル名からカメラ番号を取得（v4l2_<N>.param.yamlから<N>を抽出）
            camera_num = os.path.basename(param_file).split('_')[1].split('.')[0]
            # 設置場所を取得（frame_idからcamera_optical_linkを除去）
            location = frame_id.replace('/camera_optical_link', '')
            # 座標情報を取得
            coords = calibration_data.get(f"{location}/camera_link", {})
            # トピック名を生成
            topic = f'/sensing/camera/camera{camera_num}/image_raw/compressed'
            camera_mappings[camera_num] = (location, coords, topic)
        except Exception as e:
            print(f"Error processing {param_file}: {e}")
    
    return camera_mappings

def print_camera_mappings(mappings: Dict[str, Tuple[str, Dict, str]]):
    """
    カメラ番号と設置場所の紐付けを表示する
    Args:
        mappings: カメラ番号と設置場所、座標、トピック名の紐付け辞書
    """
    print("\nカメラ番号と設置場所の紐付け:")
    print("-" * 150)
    print("カメラ番号\t設置場所\t\t座標 (x, y, z)\t\t\tトピック名")
    print("-" * 150)
    # カメラ番号でソート
    for camera_num in sorted(mappings.keys(), key=int):
        location, coords, topic = mappings[camera_num]
        x = coords.get('x', 'N/A')
        y = coords.get('y', 'N/A')
        z = coords.get('z', 'N/A')
        # print(f"camera{camera_num}\t{location}\t({x}, {y}, {z})\t{topic}")
        print(f"{camera_num}:({y}, {x}),")

def get_camera_positions(base_path: str):
    # パスの存在確認
    if not os.path.exists(base_path):
        print(f"Error: パス {base_path} が存在しません")
        return
    # カメラマッピングを取得
    camera_mappings = find_camera_mappings(base_path)
    front_coords = []
    side_corrds = []
    ###########
    for camera_num in sorted(camera_mappings.keys(), key=int):
        _, coords, _ = camera_mappings[camera_num]
        front_coords.append(coords['y'])
        side_corrds.append(coords['x'])
    front_proj= [int((x-min(front_coords))/(max(front_coords)-min(front_coords))*500 + 110) for x in front_coords]
    side_proj= [700-int((x-min(side_corrds))/(max(side_corrds)-min(side_corrds))*500) for x in side_corrds]
    ###########
    camera_positions = {}
    for i,(f,s) in enumerate((zip(front_proj,side_proj))):
        print(f"{i}:({f}, {s}),")
        camera_positions[i] = (f, s)
    return camera_positions

if __name__ == "__main__":
    main() 