#!/bin/bash
CONTAINER_NAME=papwikires
MOUNT_DIR=$1
SRC_DUMP=$2
if [ "$2" = "." ];
then
  PRG_CMD="python -m papwikires.data_acquisition  --output_dir /data"
else
  PRG_CMD="python -m papwikires.data_acquisition --src /data/$SRC_DUMP --output_dir /data"
fi
docker build -t $CONTAINER_NAME . && docker run --rm -it -v $MOUNT_DIR:/data $CONTAINER_NAME $PRG_CMD
