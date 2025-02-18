#!/bin/bash

#export DISPLAY=:1
#export XDG_RUNTIME_DIR=/run/user/1000
#terminator

#!/bin/bash
exec > >(logger -t terminator_startup) 2>&1
export DISPLAY=:1
export XDG_RUNTIME_DIR=/run/user/1000
logger "Attempting to start Terminator"
terminator
