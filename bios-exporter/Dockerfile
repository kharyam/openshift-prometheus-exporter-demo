FROM centos:7


ADD bios-exporter.py /usr/bin
RUN yum install -y dmidecode python3 python3-pip && \
    yum clean all && \
    pip-3 install prometheus-client && \
    chmod +x /usr/bin/bios-exporter.py

EXPOSE 8000

CMD /usr/bin/bios-exporter.py
