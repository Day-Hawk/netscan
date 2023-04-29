FROM python:alpine3.17

COPY ./log4p.py /home/netscan/log4p.py
COPY ./netscan.py /home/netscan/netscan.py
WORKDIR /home/netscan

RUN chmod -Rv 7777 /home/netscan # Change permission

RUN pip install fire
RUN pip install log4python

LABEL org.opencontainers.image.source=https://github.com/Day-Hawk/netscan
LABEL org.opencontainers.image.description="Simple tool to check if an application is running under host and port."
LABEL org.opencontainers.image.licenses="Apache License 2.0"

CMD ["python3", "netscan.py"]