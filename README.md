# Project Title

***This document is still in the works.***  

Service for storing key-value pairs, similar to Redis. API is based on HTTP, resourses:  
http://<ip_addr>:<port_num>/key/<name_of_key>  
It provides 3 methods:
- read a key, HTTP/GET
- set a key, HTTP/POST
- remove a key, HTTP/DELETE

http://<ip_addr>:<port_num>/dump/  
It provides: show all keys, HTTP/GET


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

Use Python3.8

### Installing

- Copy _./src/_ in /opt/like_redis/.
- Create /opt/logs/, /opt/dump/
- Copy ini-file from _./deployment_scripts/like_redis.ini_ into /usr/local/etc/like_redis/
- Copy ini-file from _./deployment_scripts/like_redis_run.sh_ into /opt/like_redis/
- Change permissions on like_redis_run.sh to run it
- Run it

Is smth going wrong? Everything will be fine later.
