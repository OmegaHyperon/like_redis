#!/bin/sh

#
#   For inside of docker container
#
#

log_dir="./logs/"

if [ ! -d "${log_dir}" ]; then
  mkdir "${log_dir}"
fi

echo "Start of Like REDIS server"
/opt/app-root/bin/python3.8 ./like_redis.py
