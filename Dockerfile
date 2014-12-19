#dddnsupdate dockerfile
FROM python:2.7.8-onbuild

MAINTAINER Bradley Cicenas <bradley.cicenas@gmail.com>
COMMIT Docker Dynamic DNS Updater

RUN chmod +x /usr/src/app/run.sh && \
    cd /usr/src/app && \
    python setup.py install 

ENTRYPOINT [ "/usr/src/app/run.sh" ]
