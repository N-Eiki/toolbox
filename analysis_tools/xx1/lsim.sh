SCRIPT_DIR=$(cd $(dirname $0); pwd)
HOME_DIR=$(pwd)

# cd $SCRIPT_DIR
# cd ../

source ./install/setup.bash

# MAP_PATH=/home/eikinagata2/autoware_map/odaiba_rinkai/odaiba_rinkai_1291
MAP_PATH=/home/eikinagata2/autoware_map/xx1-0614
VECHILE_MODEL=jpntaxi
SENSOR_MODEL=aip_xx1
VEHICLE_ID=default


# parse arguments
for ((i=1; i<=$#; i++)); do
    if [ "${!i}" = "--map" ]; then
        let "j=i+1"
        MAP_PATH="${!j}"
        echo "MAP_PATH: ${MAP_PATH}"
    fi
done

echo "MAP_PATH: ${MAP_PATH}"


ros2 launch autoware_launch logging_simulator.launch.xml \
    map_path:=${MAP_PATH} \
    vehicle_model:=${VECHILE_MODEL} \
    vehicle_id:=${VEHICLE_ID} \
    sensor_model:=${SENSOR_MODEL}  \
    rviz:=true \
    perception:=true \
    planning:=false \
    control:=false \
    localization:=false \
    sensing:=true \
    system:=false \
    launch_vehicle_interface:=false \
    launch_driver:=false
