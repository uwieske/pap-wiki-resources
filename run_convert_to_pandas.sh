#!/bin/bash
CONTAINER_NAME=papwikires
SOURCE_DIR=$1
DUMP_FILE=$2
PRG_CMD="python -m papwikires.data_acquisition --src_file /data/$DUMP_FILE --output_dir /data"

docker build -t $CONTAINER_NAME . && docker run --rm -it -v $SOURCE_DIR:/data $CONTAINER_NAME $PRG_CMD
