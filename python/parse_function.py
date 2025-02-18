"""The library to parse the data from rosbag file."""

import sys
from collections import defaultdict

import pandas as pd
import rosbag2_py
from cv_bridge import CvBridge
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message

def parse_rosbag(rosbag_path: str, target_topic_list: list[str], custom_parser=None, limit: int = 0,) -> dict:
    serialization_format = "cdr"
    storage_options = rosbag2_py.StorageOptions(uri=rosbag_path, storage_id="sqlite3")
    converter_options = rosbag2_py.ConverterOptions(
        input_serialization_format=serialization_format,
        output_serialization_format=serialization_format,
    )

    reader = rosbag2_py.SequentialReader()
    reader.open(storage_options, converter_options)

    topic_types = reader.get_all_topics_and_types()
    type_map = {
        topic_types[i].name: topic_types[i].type for i in range(len(topic_types))
    }

    storage_filter = rosbag2_py.StorageFilter(topics=target_topic_list)
    reader.set_filter(storage_filter)

    topic_name_to_data = defaultdict(list)
    parse_num = 0
    while reader.has_next():
        (topic, data, t) = reader.read_next()
        msg_type = get_message(type_map[topic])
        msg = deserialize_message(data, msg_type)
        if topic in target_topic_list:
            parsed_msg = parse_msg(msg, msg_type, custom_parser)
            if parsed_msg is None:
                continue
            topic_name_to_data[topic].append(parsed_msg)
            parse_num += 1
            if limit > 0 and parse_num >= limit:
                break
    for key in target_topic_list:
        topic_name_to_data[key] = pd.DataFrame(topic_name_to_data[key])
        print(f"{key}: {len(topic_name_to_data[key])} msgs")
    return topic_name_to_data

def parse_msg(msg, msg_type, custom_parser):
    class_name = msg_type.__class__.__name__.replace("Metaclass_", "")
    try:
        try:
            # parse_ + クラス名 の関数を動的に取得して実行
            parser = globals()[f"parse_{class_name}"]
            return parser(msg)
        except:
            return custom_parser(msg)
    except KeyError:
        print(f"Error: {class_name} is not supported.")
        sys.exit(0)