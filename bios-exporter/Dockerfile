FROM registry.access.redhat.com/ubi8:latest

ARG EXPORTER_PORT
ENV EXPORTER_PORT ${EXPORTER_PORT:-8000}

ADD bios-exporter.py /usr/bin

RUN yum -y module install python36 \
    && pip-3 install prometheus-client \
    && chmod +x /usr/bin/bios-exporter.py

EXPOSE $EXPORTER_PORT

CMD /usr/bin/bios-exporter.py --port $EXPORTER_PORT
