#!/bin/bash

PATH_TO_AW_PROJ=/home/eikinagata2/pilot-auto/pilot-auto.x2.v3.1.0
PATH_TO_DEBUG_TOOL_DIR=/home/eikinagata2/analysis_tools/debug_tools
# DB3_FILE=0388f3fc-7d88-4520-b78f-b90befa92094_2024-07-19-13-49-55_p0900_43.db3
# DB3_FILE=0388f3fc-7d88-4520-b78f-b90befa92094_2024-07-30-15-09-56_p0900_32.db3
# DB3_FILE=0388f3fc-7d88-4520-b78f-b90befa92094_2024-08-02-11-42-04_p0900_40.db3
DB3_FILE=0388f3fc-7d88-4520-b78f-b90befa92094_2024-08-06-11-15-19_p0900_3.db3
PATH_TO_BAG_DIR=/home/eikinagata2/autoware_rosbag/x2/odaiba_rinkai/0806
cd $PATH_TO_AW_PROJ
source install/setup.bash

cd $PATH_TO_DEBUG_TOOL_DIR
bash analyze-tmux.sh \
    -b $PATH_TO_BAG_DIR/$DB3_FILE \
    -d $PATH_TO_BAG_DIR \
    -c config/sample.sh \
    -a $PATH_TO_AW_PROJ \
    -m /PATH_TO_MAP_FOLDER