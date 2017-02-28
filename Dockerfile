from python:2.7.13

COPY ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY ./mutex_agent/* /opt/bin/
RUN chmod +x /opt/bin/*
ENV PATH=$PATH:/opt/bin/
WORKDIR /home/
