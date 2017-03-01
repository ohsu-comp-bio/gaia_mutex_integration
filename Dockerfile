from python:2.7.13

ADD . /opt/mutex-agent/
RUN cd /opt/mutex-agent && \
    pip install -r requirements.txt && \
    python setup.py install
WORKDIR /home/
