#!/bin/bash

cd /home/eikinagata2/analysis_tools/autoware.benchmark_tools/tools/system_monitor_tracing

PATH_TO_AW_PROJ=/home/eikinagata2/pilot-auto/pilot-auto.x2.v3.1.0
MAP_PATH=/home/eikinagata2/autoware_map/odaiba_rinkai_1291
DB3_FILE=0388f3fc-7d88-4520-b78f-b90befa92094_2024-07-19-13-49-55_p0900_53.db3
PATH_TO_BAG_DIR=/home/eikinagata2/autoware_rosbag/x2/odaiba_rinkai/0806

./run_autoware_benchmark.bash \
    --autoware-path ${PATH_TO_AW_PROJ}\
    --map-path ${MAP_PATH} \
    --vehicle-model j6_gen1 \
    --sensor-model aip_x2 \
    -d /home/eikinagata2/analysis_tools/prod/x2/output/autoware_benchmark \
    -r 0.2 ${PATH_TO_BAG_DIR}/${DB3_FILE}