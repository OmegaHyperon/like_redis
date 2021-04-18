#!/bin/sh

log_dir="./logs/"

export LIKE_REDIS=/usr/local/etc/like_redis.ini

if [ ! -d "${log_dir}" ]; then
  mkdir "${log_dir}"
fi

echo "Start of Like REDIS server"
python3.8 ./like_redis.py
