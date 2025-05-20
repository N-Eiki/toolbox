import argparse
import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import CompressedImage

from show_pos_cameraNum import get_camera_positions

# === 定数定義 ===
WINDOW_SIZE = (500, 500)          # キャンバスサイズ
CAR_BODY_SIZE = (200, 400)        # 車体描画サイズ（width, height）
IMAGE_SIZE = (160, 120)           # 表示画像サイズ
TOP_VIEW_WINDOW_NAME = "Top-Down Camera Layout"


class ViewCameraPos(Node):
    def __init__(self, camera_positions):
        super().__init__('view_camera_pos')
        self.camera_positions = camera_positions
        self.image_dict = {}
        self.window_positioned = set()

        qos_profile = QoSProfile(depth=10)
        qos_profile.reliability = ReliabilityPolicy.BEST_EFFORT

        # カメラごとにサブスクライブ
        for cam_id in camera_positions:
            topic = f'/sensing/camera/camera{cam_id}/image_raw/compressed'
            self.create_subscription(
                CompressedImage,
                topic,
                self._create_image_callback(cam_id),
                qos_profile
            )
            self.get_logger().info(f"Subscribed to: {topic}")

        # 表示更新用タイマー
        self.create_timer(0.1, self._update_display)

    def _create_image_callback(self, cam_id):
        def callback(msg):
            try:
                np_arr = np.frombuffer(msg.data, np.uint8)
                image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                if image is not None:
                    resized = cv2.resize(image, IMAGE_SIZE)
                    self.image_dict[cam_id] = resized
            except Exception as e:
                self.get_logger().error(f"[camera{cam_id}] Image decode error: {e}")
        return callback

    def _draw_car_top_view(self, canvas):
        center_x, center_y = WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2
        car_w, car_h = CAR_BODY_SIZE

        # 車体
        top_left = (center_x - car_w // 2, center_y - car_h // 2)
        bottom_right = (center_x + car_w // 2, center_y + car_h // 2)
        cv2.rectangle(canvas, top_left, bottom_right, (50, 50, 50), -1)

        # 車輪
        wheel_offsets = [(20, 40), (-20, 40), (20, -40), (-20, -40)]
        for dx, dy in wheel_offsets:
            wheel_x = center_x + dx * car_w // 40
            wheel_y = center_y + dy * car_h // 100
            cv2.circle(canvas, (wheel_x, wheel_y), 15, (0, 0, 0), -1)

        # 前方矢印
        cv2.arrowedLine(canvas, (center_x, top_left[1]), (center_x, top_left[1] - 30), (0, 255, 0), 2)

    def _update_display(self):
        # トップビュー描画
        canvas = np.zeros((WINDOW_SIZE[1], WINDOW_SIZE[0], 3), dtype=np.uint8)
        self._draw_car_top_view(canvas)

        # 各カメラ画像描画
        for cam_id, image in self.image_dict.items():
            x, y = self.camera_positions[cam_id]
            window_name = f"camera{cam_id}"

            labeled_image = image.copy()
            cv2.putText(labeled_image, window_name, (5, 15), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 255), 1, cv2.LINE_AA)
            cv2.imshow(window_name, labeled_image)

            # 初回のみウィンドウ位置設定
            if cam_id not in self.window_positioned:
                cv2.moveWindow(window_name, x, y)
                self.window_positioned.add(cam_id)

        # トップビューウィンドウの表示と移動
        cv2.imshow(TOP_VIEW_WINDOW_NAME, canvas)
        if "top_view" not in self.window_positioned:
            cv2.moveWindow(TOP_VIEW_WINDOW_NAME, 100, 100)
            self.window_positioned.add("top_view")

        cv2.waitKey(1)


def main():
    parser = argparse.ArgumentParser(description='カメラ番号と設置場所の紐付けを表示')
    parser.add_argument('--base_path', default="/home/eikinagata2/pilot-auto/pilot-auto.x2-v4.2-20250314/src/autoware/individual_params/individual_params/config/default/aip_x2_gen2")
    args = parser.parse_args()

    camera_positions = get_camera_positions(args.base_path)

    rclpy.init(args=None)
    node = ViewCameraPos(camera_positions)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
