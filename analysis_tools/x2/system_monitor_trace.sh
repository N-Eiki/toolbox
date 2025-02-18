#!/bin/bash

PATH_TO_BAG_DIR=/home/eikinagata2/autoware_rosbag/x2/odaiba_rinkai/0806
# DB3_FILE=0388f3fc-7d88-4520-b78f-b90befa92094_2024-07-19-13-49-55_p0900_43.db3
DB3_FILE=0388f3fc-7d88-4520-b78f-b90befa92094_2024-08-06-11-15-19_p0900_3.db3


SCRIPT_DIR=$(cd $(dirname $0); pwd)

cd /home/eikinagata2/analysis_tools/autoware.benchmark_tools/tools/system_monitor_tracing
./run_system_monitor_trace.bash \
    --rosbag2 ${PATH_TO_BAG_DIR}/${DB3_FILE} \
    -d ${SCRIPT_DIR}/output/system_monitor/$1
