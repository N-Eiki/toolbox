SCRIPT_DIR=$(cd $(dirname $0); pwd)
HOME_DIR=$(pwd)


source install/setup.bash

MAP_PATH=/home/eikinagata2/autoware_map/uda-20231206
VECHILE_MODEL=robobus
SENSOR_MODEL=robobus_sensor_kit
VEHICLE_ID=default

echo "MAP_PATH: ${MAP_PATH}"

ros2 launch autoware_launch planning_simulator.launch.xml \
 map_path:=${MAP_PATH} \
 vehicle_model:=${VECHILE_MODEL} \
 sensor_model:=${SENSOR_MODEL} \
 vehicle_id:=${VEHICLE_ID}

