FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /opt/bbot

COPY ./* /opt/bbot/
COPY ./staic /opt/bbot/static
COPY ./templates /opt/bbot/templates
WORKDIR /opt/bbot

RUN pip3 --trusted-host pypi.org --trusted-host files.pythonhosted.org install --upgrade pip
RUN pip3 --trusted-host pypi.org --trusted-host files.pythonhosted.org install -r req.txt

EXPOSE 8080


RUN chmod +x /opt/bbot/start.sh


CMD ["python3", "main.py"]     