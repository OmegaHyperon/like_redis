FROM centos/python-38-centos7:latest

USER 0

RUN mkdir -p /opt/like_redis/

COPY ./src/* /opt/like_redis/
RUN echo $(ls /opt/like_redis/)

COPY ./init.d_scripts/dialer_ivr_run_docker.sh /opt/dl_ivr/
COPY ./init.d_scripts/dialer_ivr_stop.sh /opt/dl_ivr/

COPY ./distr/py/* /opt/dl_ivr/distr/py/
COPY ./distr/oic/* /opt/dl_ivr/distr/oic/

WORKDIR /opt/dl_ivr/

# Common libs
RUN pip3.8 install /opt/dl_ivr/distr/py/attrs-20.3.0-py2.py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/certifi-2020.12.5-py2.py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/chardet-3.0.4-py2.py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/cx_Oracle-8.1.0-cp38-cp38-manylinux1_x86_64.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/idna-2.10-py2.py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/json2html-1.3.0.tar.gz
RUN pip3.8 install /opt/dl_ivr/distr/py/multidict-5.1.0-cp38-cp38-manylinux2014_x86_64.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/Pillow-8.1.0-cp38-cp38-manylinux1_x86_64.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/PyJWT-2.0.0-py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/requests-2.25.1-py2.py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/singleton-decorator-1.0.0.tar.gz
RUN pip3.8 install /opt/dl_ivr/distr/py/typing_extensions-3.7.4.3-py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/urllib3-1.26.2-py2.py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/yarl-1.6.3-cp38-cp38-manylinux2014_x86_64.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/asyncio-3.4.3-py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/async_timeout-3.0.1-py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/aiohttp-3.7.3-cp38-cp38-manylinux2014_x86_64.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/aiohttp_basicauth-0.2.0-py3-none-any.whl

# for pytest
RUN pip3.8 install /opt/dl_ivr/distr/py/atomicwrites-1.4.0-py2.py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/pluggy-0.13.1-py2.py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/py-1.10.0-py2.py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/colorama-0.4.4-py2.py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/iniconfig-1.1.1-py2.py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/pyparsing-2.4.7-py2.py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/packaging-20.8-py2.py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/toml-0.10.2-py2.py3-none-any.whl
RUN pip3.8 install /opt/dl_ivr/distr/py/pytest-6.2.2-py3-none-any.whl

#
RUN echo proxy=http://127.0.0.1:3128 >> /etc/yum.conf
RUN echo >> /etc/yum.conf
RUN yum -y install libaio

RUN rpm -Uhv /opt/dl_ivr/distr/oic/oracle-instantclient19.3-basic-19.3.0.0.0-1.x86_64.rpm
RUN rpm -Uhv /opt/dl_ivr/distr/oic/oracle-instantclient19.3-sqlplus-19.3.0.0.0-1.x86_64.rpm

EXPOSE 8079
EXPOSE 8078

ENV TZ Europe/Moscow
# ENV DIALER_IVR /opt/dl_ivr/mnt/dialer-ivr-dev.ini

#RUN echo $(ls)
RUN chmod 755 ./dialer_ivr_run_docker.sh
CMD ["./dialer_ivr_run_docker.sh"]

# Сборка:
# docker build -t dl_ivr/dl_ivr:1 --build-arg https_proxy=http://127.0.0.1:3128 .

# Запуск:
# docker run -d -p 192.168.1.90:8080:8080 -v /home/user/PycharmProjects/scratches/small_http/volume:/opt/app/volume ikonst/small_http:5

# Доступ: http://192.168.1.90:8080/

